import React, { useState } from 'react';
import { Resolver } from '@/modules/resolver/Resolver';
import { useCanvasStore } from '@/store/canvasStore';
import { FlowNode } from '@/contracts/components';

interface NodeType {
  id: string;
  name: string;
  category: string;
  description: string;
  defaultConfig: Record<string, any>;
}

const NODE_TYPES: NodeType[] = [
  {
    id: 'text-input',
    name: 'Text Input',
    category: 'Input',
    description: 'Text input node',
    defaultConfig: { text: '' }
  },
  {
    id: 'text-processor',
    name: 'Text Processor',
    category: 'Processing',
    description: 'Process text data',
    defaultConfig: { operation: 'uppercase' }
  },
  {
    id: 'output',
    name: 'Output',
    category: 'Output',
    description: 'Display results',
    defaultConfig: {}
  }
];

const CATEGORIES = ['Input', 'Processing', 'Output'];

export const NodePalette: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [activeCategory, setActiveCategory] = useState('Input');
  const { addNode } = useCanvasStore();

  const filteredNodes = NODE_TYPES.filter(node => 
    node.category === activeCategory &&
    node.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleAddNode = (nodeType: NodeType) => {
    const newNode: FlowNode = {
      id: `${nodeType.id}-${Date.now()}`,
      type: nodeType.name,
      position: { x: 100, y: 100 },
      config: { ...nodeType.defaultConfig }
    };
    addNode(newNode);
  };

  return (
    <Resolver.Card className="w-64 h-full">
      <div className="p-4">
        <h3 className="text-lg font-semibold mb-4">Node Palette</h3>
        
        <Resolver.Input
          placeholder="Search nodes..."
          value={searchTerm}
          onChange={setSearchTerm}
          className="mb-4"
        />
        
        {/* Category tabs */}
        <div className="flex flex-wrap gap-1 mb-4">
          {CATEGORIES.map(category => (
            <button
              key={category}
              onClick={() => setActiveCategory(category)}
              className={`px-3 py-1 text-sm rounded transition-colors ${
                activeCategory === category
                  ? 'bg-dominant-100 text-dominant-700'
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              }`}
            >
              {category}
            </button>
          ))}
        </div>
        
        {/* Node list */}
        <div className="space-y-2">
          {filteredNodes.map(nodeType => (
            <div
              key={nodeType.id}
              className="p-3 border rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
              onClick={() => handleAddNode(nodeType)}
            >
              <div className="font-medium text-sm">{nodeType.name}</div>
              <div className="text-xs text-gray-500 mt-1">
                {nodeType.description}
              </div>
            </div>
          ))}
        </div>
        
        {filteredNodes.length === 0 && (
          <div className="text-center text-gray-500 text-sm mt-4">
            No nodes found
          </div>
        )}
      </div>
    </Resolver.Card>
  );
};