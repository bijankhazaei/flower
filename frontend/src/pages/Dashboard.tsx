import React from 'react';
import { Link } from 'react-router-dom';
import { FolderIcon, UsersIcon, PlayIcon, ChartBarIcon } from '@heroicons/react/24/outline';

const Dashboard: React.FC = () => {
  const stats = [
    { name: 'Total Projects', value: '12', icon: FolderIcon, color: 'bg-blue-500' },
    { name: 'Active Flows', value: '8', icon: PlayIcon, color: 'bg-green-500' },
    { name: 'Users', value: '24', icon: UsersIcon, color: 'bg-purple-500' },
    { name: 'Executions Today', value: '156', icon: ChartBarIcon, color: 'bg-orange-500' },
  ];

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Dashboard</h1>
        <p className="text-gray-600">Welcome to Flower - Visual Flow Builder</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat) => (
          <div key={stat.name} className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className={`${stat.color} p-3 rounded-lg`}>
                <stat.icon className="w-6 h-6 text-white" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">{stat.name}</p>
                <p className="text-2xl font-semibold text-gray-900">{stat.value}</p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Quick Actions</h2>
          <div className="space-y-3">
            <Link
              to="/projects"
              className="flex items-center p-3 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
            >
              <FolderIcon className="w-5 h-5 text-blue-600 mr-3" />
              <span className="text-blue-900">Create New Project</span>
            </Link>
            <Link
              to="/users"
              className="flex items-center p-3 bg-green-50 rounded-lg hover:bg-green-100 transition-colors"
            >
              <UsersIcon className="w-5 h-5 text-green-600 mr-3" />
              <span className="text-green-900">Manage Users</span>
            </Link>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Recent Activity</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
              <span className="text-sm">Flow "Data Processing" executed</span>
              <span className="text-xs text-gray-500">2 min ago</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
              <span className="text-sm">New user "John Doe" added</span>
              <span className="text-xs text-gray-500">1 hour ago</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
              <span className="text-sm">Project "AI Pipeline" created</span>
              <span className="text-xs text-gray-500">3 hours ago</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;