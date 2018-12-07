package main

import (
	"bytes"
	"encoding/gob"
	"errors"
	"log"
	"os"

	"github.com/influxdata/kapacitor/udf/agent"
	
	"google.golang.org/grpc"
	pb "api"
	"context"
	"time"
	"fmt"
	"strconv"
	"strings"
)

// An Agent.Handler that sends out the window state via rpc.
type windowHandler struct {
	field string
	as    string
	size  int
	state map[string]*windowState

	agent *agent.Agent
}

// The state required to keep the state
type windowState struct {
	Size   int
	Values []float64
	Timestamps []int64
}

// Update the state - pop out old values
func (a *windowState) update(value float64, timestamp int64) {
	l := len(a.Values)
	// pop out
	if a.Size == l {
		a.Values = a.Values[1:]
		a.Timestamps = a.Timestamps[1:]
	}
	a.Values = append(a.Values, value)
	a.Timestamps = append(a.Timestamps, timestamp)
}

// Convert state window to comma-separated string
// OUTPUT is: NSIZE, TIMESTAMP_VECTOR, VALUES_VECTOR
func (a *windowState) serialize() string {
	var buffer bytes.Buffer
	buffer.WriteString(fmt.Sprintf("%d,", len(a.Values)))
	for _, num := range a.Timestamps {
		buffer.WriteString(fmt.Sprintf("%d,", num))
    }
	for _, num := range a.Values {
		buffer.WriteString(fmt.Sprintf("%e,", num))
    }
    return strings.TrimSuffix(buffer.String(), ",")
}

// send state to grpc server and get response
func (a *windowState) send_to_server() float64 {
	// get address
	address := os.Getenv("ANALYTICS_SERVICE")
	
	// establish connection
	conn, err := grpc.Dial(address, grpc.WithInsecure())
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	defer conn.Close()
	c := pb.NewCalcServiceClient(conn)
	
	// Create timeout context
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	// Submit a request and parse it
	payload := a.serialize()
	r, err := c.Calculate(ctx, &pb.Request{Payload: payload})
	if err != nil {
		log.Fatalf("Calculation failure: %v", err)
	}
	s, err := strconv.ParseFloat(r.Payload, 64)
	if err != nil {
		log.Fatalf("Parsing failure: %v", err)
	}
	return s
}

func newWindowHandler(a *agent.Agent) *windowHandler {
	return &windowHandler{
		state: make(map[string]*windowState),
		as:    "window",
		agent: a,
	}
}

// Return the InfoResponse. Describing the properties of this UDF agent.
func (a *windowHandler) Info() (*agent.InfoResponse, error) {
	info := &agent.InfoResponse{
		Wants:    agent.EdgeType_STREAM,
		Provides: agent.EdgeType_STREAM,
		Options: map[string]*agent.OptionInfo{
			"field": {ValueTypes: []agent.ValueType{agent.ValueType_STRING}},
			"size":  {ValueTypes: []agent.ValueType{agent.ValueType_INT}},
			"as":    {ValueTypes: []agent.ValueType{agent.ValueType_STRING}},
		},
	}
	return info, nil
}

// Initialze the handler based of the provided options.
func (a *windowHandler) Init(r *agent.InitRequest) (*agent.InitResponse, error) {
	init := &agent.InitResponse{
		Success: true,
		Error:   "",
	}
	for _, opt := range r.Options {
		switch opt.Name {
		case "field":
			a.field = opt.Values[0].Value.(*agent.OptionValue_StringValue).StringValue
		case "size":
			a.size = int(opt.Values[0].Value.(*agent.OptionValue_IntValue).IntValue)
		case "as":
			a.as = opt.Values[0].Value.(*agent.OptionValue_StringValue).StringValue
		}
	}

	if a.field == "" {
		init.Success = false
		init.Error += " must supply field"
	}
	if a.size == 0 {
		init.Success = false
		init.Error += " must supply window size"
	}
	if a.as == "" {
		init.Success = false
		init.Error += " invalid as name provided"
	}

	return init, nil
}

// Create a snapshot of the running state of the process.
func (a *windowHandler) Snapshot() (*agent.SnapshotResponse, error) {
	var buf bytes.Buffer
	enc := gob.NewEncoder(&buf)
	enc.Encode(a.state)

	return &agent.SnapshotResponse{
		Snapshot: buf.Bytes(),
	}, nil
}

// Restore a previous snapshot.
func (a *windowHandler) Restore(req *agent.RestoreRequest) (*agent.RestoreResponse, error) {
	buf := bytes.NewReader(req.Snapshot)
	dec := gob.NewDecoder(buf)
	err := dec.Decode(&a.state)
	msg := ""
	if err != nil {
		msg = err.Error()
	}
	return &agent.RestoreResponse{
		Success: err == nil,
		Error:   msg,
	}, nil
}

// Receive a point and update window
// Send a response with result from analytics service
func (a *windowHandler) Point(p *agent.Point) error {
	// Update the moving average.
	value := p.FieldsDouble[a.field]
	timestamp := p.Time
	state := a.state[p.Group]
	if state == nil {
		state = &windowState{Size: a.size}
		a.state[p.Group] = state
	}
	state.update(value, timestamp)
	
	// submit to grpc and get the result
	result := state.send_to_server()

	// Re-use the existing point so we keep the same tags etc.
	p.FieldsDouble = map[string]float64{a.as: result}
	p.FieldsInt = nil
	p.FieldsString = nil
	// Send point with average value.
	a.agent.Responses <- &agent.Response{
		Message: &agent.Response_Point{
			Point: p,
		},
	}
	return nil
}

// This handler does not do batching
func (a *windowHandler) BeginBatch(*agent.BeginBatch) error {
	return errors.New("batching not supported")
}

// This handler does not do batching
func (a *windowHandler) EndBatch(*agent.EndBatch) error {
	return errors.New("batching not supported")
}

// Stop the handler gracefully.
func (a *windowHandler) Stop() {
	close(a.agent.Responses)
}

func main() {
	a := agent.New(os.Stdin, os.Stdout)
	h := newWindowHandler(a)
	a.Handler = h

	log.Println("Starting agent")
	a.Start()
	err := a.Wait()
	if err != nil {
		log.Fatal(err)
	}
}