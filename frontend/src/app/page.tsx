'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function HomePage() {
  const router = useRouter();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('access_token');
    setIsLoggedIn(!!token);

    // If logged in, redirect to tasks page after a short delay
    if (token) {
      const timer = setTimeout(() => {
        router.push('/tasks');
      }, 2000);
      return () => clearTimeout(timer);
    }
  }, [router]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Welcome to <span className="text-indigo-600">Todo App</span>
          </h1>
          <p className="text-lg md:text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
            Organize your tasks, boost your productivity. Get started today and take control of your daily activities.
          </p>

          <div className="flex flex-col sm:flex-row justify-center gap-4 mb-16">
            {!isLoggedIn ? (
              <>
                <Link
                  href="/signup"
                  className="px-8 py-4 bg-indigo-600 text-white font-semibold rounded-lg shadow-lg hover:bg-indigo-700 transition duration-300 transform hover:scale-105"
                >
                  Get Started
                </Link>
                <Link
                  href="/login"
                  className="px-8 py-4 bg-white text-indigo-600 font-semibold rounded-lg shadow-lg border border-indigo-200 hover:bg-indigo-50 transition duration-300"
                >
                  Sign In
                </Link>
              </>
            ) : (
              <div className="text-lg text-gray-700">
                You are logged in. Redirecting to your tasks...
              </div>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16">
            <div className="bg-white p-6 rounded-xl shadow-md">
              <div className="text-indigo-600 text-3xl mb-3">✓</div>
              <h3 className="text-xl font-semibold mb-2">Task Management</h3>
              <p className="text-gray-600">Easily create, edit, and organize your tasks</p>
            </div>
            <div className="bg-white p-6 rounded-xl shadow-md">
              <div className="text-indigo-600 text-3xl mb-3">🔔</div>
              <h3 className="text-xl font-semibold mb-2">Reminders</h3>
              <p className="text-gray-600">Never miss a deadline with due date reminders</p>
            </div>
            <div className="bg-white p-6 rounded-xl shadow-md">
              <div className="text-indigo-600 text-3xl mb-3">🔒</div>
              <h3 className="text-xl font-semibold mb-2">Secure</h3>
              <p className="text-gray-600">Your data is protected with industry-standard security</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}