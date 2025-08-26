import React, { useState } from 'react';
import { Resolver } from '@/modules/resolver/Resolver';
import { useCanvasStore } from '@/store/canvasStore';

interface FlowCompilerProps {
  isOpen: boolean;
  onClose: () => void;
}

export const FlowCompiler: React.FC<FlowCompilerProps> = ({ isOpen, onClose }) => {
  const { nodes, connections } = useCanvasStore();
  const [isCompiling, setIsCompiling] = useState(false);
  const [compiledCode, setCompiledCode] = useState<string>('');
  const [error, setError] = useState<string>('');

  const compileFlow = async () => {
    setIsCompiling(true);
    setError('');
    
    try {
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const mockCode = `# Generated Flow Code
def execute_flow():
${Object.values(nodes).map(node => `    # ${node.type}: ${node.id}`).join('\n')}
    
    results = {}
${Object.values(nodes).map(node => `    results['${node.id}'] = process_node('${node.id}')`).join('\n')}
    
    return results`;

      setCompiledCode(mockCode);
    } catch (err) {
      setError('Compilation failed');
    } finally {
      setIsCompiling(false);
    }
  };

  return (
    <Resolver.Modal isOpen={isOpen} onClose={onClose} title="Flow Compiler" size="lg">
      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <div className="text-sm text-gray-600">
            {Object.keys(nodes).length} nodes, {Object.keys(connections).length} connections
          </div>
          <Resolver.Button
            onClick={compileFlow}
            loading={isCompiling}
            disabled={Object.keys(nodes).length === 0}
          >
            Compile Flow
          </Resolver.Button>
        </div>

        {error && (
          <div className="p-3 bg-error-50 border border-error-200 rounded text-error-700 text-sm">
            {error}
          </div>
        )}

        {compiledCode && (
          <pre className="bg-gray-50 p-4 rounded text-sm overflow-auto max-h-96 border">
            <code>{compiledCode}</code>
          </pre>
        )}
      </div>
    </Resolver.Modal>
  );
};