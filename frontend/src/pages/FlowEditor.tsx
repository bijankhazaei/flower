import React, { useState, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import ReactFlow, {
  Node,
  Edge,
  addEdge,
  Connection,
  useNodesState,
  useEdgesState,
  Controls,
  MiniMap,
  Background,
} from 'reactflow';
import { PlayIcon, StopIcon, DocumentArrowDownIcon } from '@heroicons/react/24/outline';

const initialNodes: Node[] = [
  {
    id: '1',
    type: 'input',
    data: { label: 'Start' },
    position: { x: 250, y: 25 },
  },
];

const initialEdges: Edge[] = [];

const FlowEditor: React.FC = () => {
  const { id: projectId, flowId } = useParams();
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [isRunning, setIsRunning] = useState(false);

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const addNode = (type: string) => {
    const newNode: Node = {
      id: `${nodes.length + 1}`,
      type,
      data: { label: `${type} Node` },
      position: { x: Math.random() * 400, y: Math.random() * 400 },
    };
    setNodes((nds) => [...nds, newNode]);
  };

  const saveFlow = async () => {
    try {
      // Save flow logic here
      console.log('Saving flow...', { nodes, edges });
    } catch (error) {
      console.error('Failed to save flow:', error);
    }
  };

  const runFlow = async () => {
    setIsRunning(true);
    try {
      // Execute flow logic here
      console.log('Running flow...', { nodes, edges });
      setTimeout(() => setIsRunning(false), 2000);
    } catch (error) {
      console.error('Failed to run flow:', error);
      setIsRunning(false);
    }
  };

  return (
    <div className="h-screen flex flex-col">
      {/* Toolbar */}
      <div className="bg-white border-b p-4 flex justify-between items-center">
        <div className="flex items-center gap-4">
          <h1 className="text-lg font-semibold">Flow Editor</h1>
          <div className="flex gap-2">
            <button
              onClick={() => addNode('default')}
              className="px-3 py-1 bg-gray-100 rounded text-sm hover:bg-gray-200"
            >
              + Process
            </button>
            <button
              onClick={() => addNode('output')}
              className="px-3 py-1 bg-gray-100 rounded text-sm hover:bg-gray-200"
            >
              + Output
            </button>
          </div>
        </div>
        
        <div className="flex gap-2">
          <button
            onClick={saveFlow}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            <DocumentArrowDownIcon className="w-4 h-4" />
            Save
          </button>
          <button
            onClick={runFlow}
            disabled={isRunning}
            className={`flex items-center gap-2 px-4 py-2 rounded ${
              isRunning
                ? 'bg-gray-400 text-white cursor-not-allowed'
                : 'bg-green-600 text-white hover:bg-green-700'
            }`}
          >
            {isRunning ? (
              <>
                <StopIcon className="w-4 h-4" />
                Running...
              </>
            ) : (
              <>
                <PlayIcon className="w-4 h-4" />
                Run
              </>
            )}
          </button>
        </div>
      </div>

      {/* Flow Canvas */}
      <div className="flex-1">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          fitView
        >
          <Controls />
          <MiniMap />
          <Background variant="dots" gap={12} size={1} />
        </ReactFlow>
      </div>

      {/* Node Properties Panel */}
      <div className="w-80 bg-white border-l p-4">
        <h3 className="font-semibold mb-4">Node Properties</h3>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-1">Node Type</label>
            <select className="w-full p-2 border rounded">
              <option>HTTP Request</option>
              <option>Data Transform</option>
              <option>Condition</option>
              <option>Loop</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Configuration</label>
            <textarea
              className="w-full p-2 border rounded h-32"
              placeholder="Node configuration..."
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default FlowEditor;