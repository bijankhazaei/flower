import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { PlusIcon, PlayIcon } from '@heroicons/react/24/outline';
import { projectService } from '../services/api';

interface Project {
  id: string;
  name: string;
  description: string;
  flows: Flow[];
  created_at: string;
}

interface Flow {
  id: string;
  name: string;
  status: 'draft' | 'active' | 'paused';
}

const Projects: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newProject, setNewProject] = useState({ name: '', description: '' });

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      const data = await projectService.getAll();
      setProjects(data);
    } catch (error) {
      console.error('Failed to load projects:', error);
    }
  };

  const createProject = async () => {
    try {
      await projectService.create(newProject);
      setShowCreateModal(false);
      setNewProject({ name: '', description: '' });
      loadProjects();
    } catch (error) {
      console.error('Failed to create project:', error);
    }
  };

  const createFlow = async (projectId: string) => {
    try {
      const flowData = { name: 'New Flow', project_id: projectId };
      await projectService.createFlow(projectId, flowData);
      loadProjects();
    } catch (error) {
      console.error('Failed to create flow:', error);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Projects</h1>
        <button
          onClick={() => setShowCreateModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700"
        >
          <PlusIcon className="w-4 h-4" />
          New Project
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {projects.map((project) => (
          <div key={project.id} className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-2">{project.name}</h3>
            <p className="text-gray-600 mb-4">{project.description}</p>
            
            <div className="mb-4">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm font-medium">Flows ({project.flows?.length || 0})</span>
                <button
                  onClick={() => createFlow(project.id)}
                  className="text-blue-600 hover:text-blue-800 text-sm"
                >
                  + Add Flow
                </button>
              </div>
              
              {project.flows?.map((flow) => (
                <Link
                  key={flow.id}
                  to={`/projects/${project.id}/flows/${flow.id}`}
                  className="flex items-center justify-between p-2 hover:bg-gray-50 rounded"
                >
                  <span className="text-sm">{flow.name}</span>
                  <div className="flex items-center gap-2">
                    <span className={`px-2 py-1 text-xs rounded ${
                      flow.status === 'active' ? 'bg-green-100 text-green-800' :
                      flow.status === 'paused' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {flow.status}
                    </span>
                    <PlayIcon className="w-4 h-4 text-gray-400" />
                  </div>
                </Link>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Create Project Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="bg-white rounded-lg p-6 w-96">
            <h2 className="text-lg font-semibold mb-4">Create New Project</h2>
            <input
              type="text"
              placeholder="Project Name"
              value={newProject.name}
              onChange={(e) => setNewProject({ ...newProject, name: e.target.value })}
              className="w-full p-2 border rounded mb-3"
            />
            <textarea
              placeholder="Description"
              value={newProject.description}
              onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
              className="w-full p-2 border rounded mb-4 h-20"
            />
            <div className="flex gap-2">
              <button
                onClick={createProject}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
              >
                Create
              </button>
              <button
                onClick={() => setShowCreateModal(false)}
                className="bg-gray-300 text-gray-700 px-4 py-2 rounded hover:bg-gray-400"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Projects;