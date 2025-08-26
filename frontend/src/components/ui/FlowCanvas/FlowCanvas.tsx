import React, { useCallback } from 'react';
import { Resolver } from '@/modules/resolver/Resolver';
import { useCanvasStore } from '@/store/canvasStore';

export const FlowCanvas: React.FC = () => {
  const {
    zoom,
    pan,
    nodes,
    connections,
    selection,
    mode,
    updateNode,
    selectNodes,
    clearSelection
  } = useCanvasStore();
  
  const handleCanvasClick = useCallback(() => {
    clearSelection();
  }, [clearSelection]);
  
  const handleNodeClick = useCallback((nodeId: string) => {
    selectNodes([nodeId]);
  }, [selectNodes]);
  
  const handleNodeDrag = useCallback((nodeId: string, offset: { x: number; y: number }) => {
    const node = nodes[nodeId];
    if (node) {
      updateNode(nodeId, {
        position: {
          x: node.position.x + offset.x,
          y: node.position.y + offset.y
        }
      });
    }
  }, [nodes, updateNode]);
  
  return (
    <div className="relative w-full h-full">
      <Resolver.Canvas
        zoom={zoom}
        pan={pan}
        mode={mode}
        onCanvasClick={handleCanvasClick}
        className="w-full h-full"
      >
        {/* Connections layer */}
        <svg className="absolute inset-0 pointer-events-none">
          {Object.values(connections).map(connection => (
            <Resolver.Connection
              key={connection.id}
              connection={connection}
              nodes={nodes}
            />
          ))}
        </svg>
        
        {/* Nodes layer */}
        {Object.values(nodes).map(node => (
          <Resolver.Node
            key={node.id}
            node={node}
            isSelected={selection.includes(node.id)}
            onClick={handleNodeClick}
            onDrag={(offset) => handleNodeDrag(node.id, offset)}
          />
        ))}
      </Resolver.Canvas>
      
      {/* Canvas controls */}
      <div className="absolute bottom-4 right-4 flex flex-col gap-2">
        <Resolver.Button
          variant="secondary"
          size="sm"
          onClick={() => useCanvasStore.getState().setZoom(1)}
        >
          Reset Zoom
        </Resolver.Button>
      </div>
    </div>
  );
};