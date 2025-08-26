import React from 'react';
import { Resolver } from '@/modules/resolver/Resolver';
import { useCanvasStore } from '@/store/canvasStore';

export const PropertyPanel: React.FC = () => {
  const { nodes, selection, updateNode } = useCanvasStore();
  
  const selectedNode = selection.length === 1 ? nodes[selection[0]] : null;

  const handleConfigChange = (key: string, value: any) => {
    if (selectedNode) {
      updateNode(selectedNode.id, {
        config: {
          ...selectedNode.config,
          [key]: value
        }
      });
    }
  };

  if (!selectedNode) {
    return (
      <Resolver.Card className="w-64 h-full">
        <div className="p-4">
          <h3 className="text-lg font-semibold mb-4">Properties</h3>
          <div className="text-center text-gray-500 text-sm">
            Select a node to edit properties
          </div>
        </div>
      </Resolver.Card>
    );
  }

  return (
    <Resolver.Card className="w-64 h-full">
      <div className="p-4">
        <h3 className="text-lg font-semibold mb-4">Properties</h3>
        
        {/* Node info */}
        <div className="mb-4 p-3 bg-gray-50 rounded">
          <div className="font-medium text-sm">{selectedNode.type}</div>
          <div className="text-xs text-gray-500">ID: {selectedNode.id}</div>
        </div>
        
        {/* Position */}
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">Position</label>
          <div className="grid grid-cols-2 gap-2">
            <Resolver.Input
              type="number"
              placeholder="X"
              value={selectedNode.position.x.toString()}
              onChange={(value) => updateNode(selectedNode.id, {
                position: { ...selectedNode.position, x: parseInt(value) || 0 }
              })}
            />
            <Resolver.Input
              type="number"
              placeholder="Y"
              value={selectedNode.position.y.toString()}
              onChange={(value) => updateNode(selectedNode.id, {
                position: { ...selectedNode.position, y: parseInt(value) || 0 }
              })}
            />
          </div>
        </div>
        
        {/* Configuration */}
        <div className="mb-4">
          <label className="block text-sm font-medium mb-2">Configuration</label>
          <div className="space-y-2">
            {Object.entries(selectedNode.config).map(([key, value]) => (
              <div key={key}>
                <label className="block text-xs text-gray-600 mb-1">
                  {key}
                </label>
                <Resolver.Input
                  value={typeof value === 'string' ? value : JSON.stringify(value)}
                  onChange={(newValue) => {
                    try {
                      const parsed = JSON.parse(newValue);
                      handleConfigChange(key, parsed);
                    } catch {
                      handleConfigChange(key, newValue);
                    }
                  }}
                />
              </div>
            ))}
          </div>
        </div>
        
        {/* Actions */}
        <div className="space-y-2">
          <Resolver.Button
            variant="destructive"
            size="sm"
            onClick={() => {
              const { deleteNode, clearSelection } = useCanvasStore.getState();
              deleteNode(selectedNode.id);
              clearSelection();
            }}
            className="w-full"
          >
            Delete Node
          </Resolver.Button>
        </div>
      </div>
    </Resolver.Card>
  );
};