import Link from 'next/link'
import { ArrowRight, BarChart3, MapPin, MessageSquare, Waves } from 'lucide-react'

export default function HomePage() {
  return (
    <div className="min-h-screen">
      {/* Navigation */}
      <nav className="border-b bg-white/80 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center space-x-2">
              <Waves className="h-8 w-8 text-primary-600" />
              <span className="text-xl font-bold text-gray-900">FloatChat</span>
            </div>
            <div className="flex space-x-4">
              <Link href="/dashboard" className="text-gray-600 hover:text-primary-600 transition-colors">
                Dashboard
              </Link>
              <Link href="/chat" className="text-gray-600 hover:text-primary-600 transition-colors">
                Chat
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto text-center">
          <div className="animate-fade-in">
            <h1 className="text-5xl font-bold text-gray-900 mb-6">
              Explore Ocean Data with
              <span className="text-primary-600 block mt-2">AI-Powered Insights</span>
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              FloatChat brings conversational AI to oceanographic research. Explore ARGO float data 
              from the Indian Ocean with natural language queries and interactive visualizations.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link href="/dashboard" className="btn-primary inline-flex items-center text-lg px-8 py-3">
                View Dashboard
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
              <Link href="/chat" className="btn-secondary inline-flex items-center text-lg px-8 py-3">
                Start Chatting
                <MessageSquare className="ml-2 h-5 w-5" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Powerful Tools for Ocean Science
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Comprehensive suite of tools for analyzing ARGO float data with modern web technologies
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="card card-hover text-center animate-slide-up">
              <div className="flex justify-center mb-4">
                <div className="p-3 bg-primary-100 rounded-full">
                  <MapPin className="h-8 w-8 text-primary-600" />
                </div>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Interactive Maps</h3>
              <p className="text-gray-600">
                Visualize float locations and oceanographic data on interactive maps with 
                seamless pan and zoom capabilities.
              </p>
            </div>
            
            <div className="card card-hover text-center animate-slide-up" style={{ animationDelay: '0.1s' }}>
              <div className="flex justify-center mb-4">
                <div className="p-3 bg-ocean-100 rounded-full">
                  <BarChart3 className="h-8 w-8 text-ocean-600" />
                </div>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">Rich Visualizations</h3>
              <p className="text-gray-600">
                Time series plots, vertical profiles, and heatmaps to explore temperature, 
                salinity, and heat content patterns.
              </p>
            </div>
            
            <div className="card card-hover text-center animate-slide-up" style={{ animationDelay: '0.2s' }}>
              <div className="flex justify-center mb-4">
                <div className="p-3 bg-purple-100 rounded-full">
                  <MessageSquare className="h-8 w-8 text-purple-600" />
                </div>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-3">AI Chat Interface</h3>
              <p className="text-gray-600">
                Ask questions in natural language and get intelligent responses based on 
                the oceanographic data using advanced AI.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Data Overview */}
      <section className="py-20 bg-gradient-to-br from-primary-50 to-ocean-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Indian Ocean ARGO Data Coverage
            </h2>
            <p className="text-lg text-gray-600">
              Explore comprehensive oceanographic measurements from 2010-2013
            </p>
          </div>
          
          <div className="grid md:grid-cols-4 gap-6">
            <div className="text-center p-6 bg-white rounded-lg shadow-sm">
              <div className="text-2xl font-bold text-primary-600 mb-2">60°E - 100°E</div>
              <div className="text-gray-600">Longitude Coverage</div>
            </div>
            <div className="text-center p-6 bg-white rounded-lg shadow-sm">
              <div className="text-2xl font-bold text-ocean-600 mb-2">2010-2013</div>
              <div className="text-gray-600">Time Period</div>
            </div>
            <div className="text-center p-6 bg-white rounded-lg shadow-sm">
              <div className="text-2xl font-bold text-purple-600 mb-2">26-31°C</div>
              <div className="text-gray-600">Temperature Range</div>
            </div>
            <div className="text-center p-6 bg-white rounded-lg shadow-sm">
              <div className="text-2xl font-bold text-green-600 mb-2">34-36 PSU</div>
              <div className="text-gray-600">Salinity Range</div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <Waves className="h-6 w-6" />
              <span className="text-lg font-semibold">FloatChat</span>
            </div>
            <div className="text-gray-400 text-sm">
              © 2025 FloatChat. Ocean data exploration platform.
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}