import React, { useState } from 'react';
import { Resolver } from '@/modules/resolver/Resolver';
import { useCanvasStore } from '@/store/canvasStore';

interface FlowExecutorProps {
  isOpen: boolean;
  onClose: () => void;
}

export const FlowExecutor: React.FC<FlowExecutorProps> = ({ isOpen, onClose }) => {
  const { nodes, connections } = useCanvasStore();
  const [isExecuting, setIsExecuting] = useState(false);
  const [inputs, setInputs] = useState<Record<string, string>>({});
  const [results, setResults] = useState<any>(null);
  const [error, setError] = useState<string>('');

  const executeFlow = async () => {
    setIsExecuting(true);
    setError('');
    setResults(null);
    
    try {
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      const mockResults = {
        execution_id: 'exec_' + Date.now(),
        status: 'completed',
        results: Object.values(nodes).reduce((acc, node) => ({
          ...acc,
          [node.id]: `Result from ${node.type}`
        }), {}),
        execution_time: '1.2s'
      };

      setResults(mockResults);
    } catch (err) {
      setError('Execution failed');
    } finally {
      setIsExecuting(false);
    }
  };

  const inputNodes = Object.values(nodes).filter(node => 
    node.type.toLowerCase().includes('input')
  );

  return (
    <Resolver.Modal isOpen={isOpen} onClose={onClose} title="Execute Flow" size="lg">
      <div className="space-y-4">
        {/* Input Parameters */}
        {inputNodes.length > 0 && (
          <div>
            <h4 className="font-medium mb-3">Input Parameters</h4>
            <div className="space-y-3">
              {inputNodes.map(node => (
                <div key={node.id}>
                  <label className="block text-sm font-medium mb-1">
                    {node.type} ({node.id})
                  </label>
                  <Resolver.Input
                    placeholder={`Enter value for ${node.type}`}
                    value={inputs[node.id] || ''}
                    onChange={(value) => setInputs(prev => ({ ...prev, [node.id]: value }))}
                  />
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Execute Button */}
        <div className="flex justify-between items-center">
          <div className="text-sm text-gray-600">
            Ready to execute {Object.keys(nodes).length} nodes
          </div>
          <Resolver.Button
            onClick={executeFlow}
            loading={isExecuting}
            disabled={Object.keys(nodes).length === 0}
          >
            {isExecuting ? 'Executing...' : 'Run Flow'}
          </Resolver.Button>
        </div>

        {/* Error Display */}
        {error && (
          <div className="p-3 bg-error-50 border border-error-200 rounded text-error-700 text-sm">
            {error}
          </div>
        )}

        {/* Results Display */}
        {results && (
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <h4 className="font-medium">Execution Results</h4>
              <div className="text-sm text-complement-600">
                Status: {results.status} • Time: {results.execution_time}
              </div>
            </div>
            
            <div className="bg-gray-50 p-4 rounded border">
              <div className="text-sm font-medium mb-2">Node Results:</div>
              <div className="space-y-2">
                {Object.entries(results.results).map(([nodeId, result]) => (
                  <div key={nodeId} className="flex justify-between text-sm">
                    <span className="font-mono text-gray-600">{nodeId}:</span>
                    <span>{String(result)}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="text-xs text-gray-500">
              Execution ID: {results.execution_id}
            </div>
          </div>
        )}

        {/* Empty State */}
        {!results && !error && !isExecuting && (
          <div className="text-center py-8 text-gray-500">
            Configure input parameters and click "Run Flow" to execute
          </div>
        )}
      </div>
    </Resolver.Modal>
  );
};