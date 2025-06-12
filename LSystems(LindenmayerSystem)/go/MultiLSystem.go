package MultiLSystem

import (
	"fmt"
	"sync"
)

type MultiBatchLSystem struct {
	Configs []*LSystemConfig
}

func NewMultiBatchLSystem(configs []*LSystemConfig) *MultiBatchLSystem {
	return &MultiBatchLSystem{
		Configs: configs,
	}
}

func (m *MultiBatchLSystem) RunAll() {
	var wg sync.WaitGroup
	for _, config := range m.Configs {
		wg.Add(1)
		go func(conf *LSystemConfig) {
			defer wg.Done()
			lsystem := NewLSystem(conf)
			err := lsystem.Run()
			if err != nil {
				fmt.Printf("Error running L-System for %s: %v\n", conf.Filename, err)
			} else {
				fmt.Printf("L-System image saved as %s\n", conf.Filename)
			}
		}(config)
	}
	wg.Wait()
}
