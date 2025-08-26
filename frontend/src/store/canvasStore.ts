import { create } from 'zustand';
import { FlowNode, Connection } from '@/contracts/components';

interface CanvasState {
  // Viewport state
  zoom: number;
  pan: { x: number; y: number };
  
  // Interaction state
  mode: 'select' | 'connect' | 'pan' | 'add-node';
  selection: string[];
  
  // Canvas data
  nodes: Record<string, FlowNode>;
  connections: Record<string, Connection>;
  
  // Actions
  setZoom: (zoom: number) => void;
  setPan: (pan: { x: number; y: number }) => void;
  setMode: (mode: 'select' | 'connect' | 'pan' | 'add-node') => void;
  
  // Node operations
  addNode: (node: FlowNode) => void;
  updateNode: (id: string, updates: Partial<FlowNode>) => void;
  deleteNode: (id: string) => void;
  
  // Selection operations
  selectNodes: (nodeIds: string[]) => void;
  clearSelection: () => void;
  
  // Bulk operations
  loadFlow: (nodes: FlowNode[], connections: Connection[]) => void;
  clearCanvas: () => void;
}

export const useCanvasStore = create<CanvasState>((set, get) => ({
  // Initial state
  zoom: 1,
  pan: { x: 0, y: 0 },
  mode: 'select',
  selection: [],
  nodes: {},
  connections: {},
  
  // Actions
  setZoom: (zoom) => set({ zoom: Math.max(0.1, Math.min(3, zoom)) }),
  setPan: (pan) => set({ pan }),
  setMode: (mode) => set({ mode }),
  
  // Node operations
  addNode: (node) => set((state) => ({
    nodes: { ...state.nodes, [node.id]: node }
  })),
  
  updateNode: (id, updates) => set((state) => ({
    nodes: {
      ...state.nodes,
      [id]: { ...state.nodes[id], ...updates }
    }
  })),
  
  deleteNode: (id) => set((state) => {
    const { [id]: deleted, ...nodes } = state.nodes;
    const connections = Object.fromEntries(
      Object.entries(state.connections).filter(
        ([_, conn]) => conn.source !== id && conn.target !== id
      )
    );
    return { nodes, connections };
  }),
  
  // Selection operations
  selectNodes: (nodeIds) => set({ selection: nodeIds }),
  clearSelection: () => set({ selection: [] }),
  
  // Bulk operations
  loadFlow: (nodes, connections) => set({
    nodes: nodes.reduce((acc, node) => ({ ...acc, [node.id]: node }), {}),
    connections: connections.reduce((acc, conn) => ({ ...acc, [conn.id]: conn }), {}),
    selection: []
  }),
  
  clearCanvas: () => set({
    nodes: {},
    connections: {},
    selection: []
  })
}));