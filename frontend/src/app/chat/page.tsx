'use client'

import { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, Loader2, BarChart3, MapPin, Thermometer } from 'lucide-react'
import { apiClient } from '../../lib/api-client'

interface Message {
  id: string
  content: string
  sender: 'user' | 'bot'
  timestamp: Date
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: "Hello! I'm your ARGO float data assistant. I can help you explore ocean temperature, salinity, and heat content data from the Indian Ocean (2010-2013). Try asking me about temperature trends, spatial patterns, or specific measurements!",
      sender: 'bot',
      timestamp: new Date()
    }
  ])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      sender: 'user',
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsLoading(true)

    try {
      const response = await apiClient.chatWithData({ message: inputValue })
      
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.response,
        sender: 'bot',
        timestamp: new Date()
      }

      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Chat error:', error)
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: "I apologize, but I encountered an error processing your question. Please try again or rephrase your query.",
        sender: 'bot',
        timestamp: new Date()
      }

      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const suggestedQuestions = [
    "What is the average temperature at 60°E longitude in 2012?",
    "How does heat content vary between 60°E and 80°E?", 
    "Show me the salinity trends in the surface waters",
    "What are the typical temperature ranges in this dataset?"
  ]

  const handleSuggestionClick = (question: string) => {
    setInputValue(question)
    inputRef.current?.focus()
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between py-6">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">FloatChat</h1>
              <p className="text-gray-600 mt-1">AI assistant for ARGO float data</p>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-500">
              <div className="flex items-center space-x-1">
                <div className="h-2 w-2 bg-green-500 rounded-full"></div>
                <span>Online</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Chat Container */}
      <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full px-4 sm:px-6 lg:px-8">
        {/* Messages Area */}
        <div className="flex-1 py-6 overflow-hidden">
          <div className="h-full overflow-y-auto space-y-4 pr-2">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex items-start space-x-3 ${
                  message.sender === 'user' ? 'justify-end' : 'justify-start'
                }`}
              >
                {message.sender === 'bot' && (
                  <div className="flex-shrink-0">
                    <div className="h-8 w-8 bg-primary-100 rounded-full flex items-center justify-center">
                      <Bot className="h-5 w-5 text-primary-600" />
                    </div>
                  </div>
                )}
                
                <div
                  className={`max-w-2xl px-4 py-3 rounded-lg ${
                    message.sender === 'user'
                      ? 'bg-primary-600 text-white'
                      : 'bg-white border shadow-sm'
                  }`}
                >
                  <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                  <div className={`text-xs mt-2 ${
                    message.sender === 'user' ? 'text-primary-100' : 'text-gray-500'
                  }`}>
                    {message.timestamp.toLocaleTimeString()}
                  </div>
                </div>

                {message.sender === 'user' && (
                  <div className="flex-shrink-0">
                    <div className="h-8 w-8 bg-gray-100 rounded-full flex items-center justify-center">
                      <User className="h-5 w-5 text-gray-600" />
                    </div>
                  </div>
                )}
              </div>
            ))}
            
            {isLoading && (
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0">
                  <div className="h-8 w-8 bg-primary-100 rounded-full flex items-center justify-center">
                    <Bot className="h-5 w-5 text-primary-600" />
                  </div>
                </div>
                <div className="bg-white border shadow-sm px-4 py-3 rounded-lg">
                  <div className="flex items-center space-x-2">
                    <Loader2 className="h-4 w-4 animate-spin text-primary-600" />
                    <span className="text-sm text-gray-600">Analyzing data...</span>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Suggested Questions */}
        {messages.length === 1 && (
          <div className="py-4 border-t bg-white rounded-t-lg">
            <h3 className="text-sm font-medium text-gray-700 mb-3 px-4">Try asking about:</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 px-4">
              {suggestedQuestions.map((question, index) => (
                <button
                  key={index}
                  onClick={() => handleSuggestionClick(question)}
                  className="text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors duration-200 text-sm border"
                >
                  <div className="flex items-center space-x-2">
                    {index === 0 && <Thermometer className="h-4 w-4 text-orange-500" />}
                    {index === 1 && <BarChart3 className="h-4 w-4 text-blue-500" />}
                    {index === 2 && <MapPin className="h-4 w-4 text-green-500" />}
                    {index === 3 && <Bot className="h-4 w-4 text-purple-500" />}
                    <span className="text-gray-700">{question}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input Area */}
        <div className="py-4 bg-white border-t">
          <div className="flex items-center space-x-3">
            <div className="flex-1 relative">
              <input
                ref={inputRef}
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about ocean temperature, salinity, or heat content..."
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                disabled={isLoading}
              />
            </div>
            <button
              onClick={handleSendMessage}
              disabled={!inputValue.trim() || isLoading}
              className="btn-primary p-3 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="h-5 w-5" />
            </button>
          </div>
          
          <div className="mt-2 text-xs text-gray-500 px-4">
            Press Enter to send, Shift+Enter for new line
          </div>
        </div>
      </div>
    </div>
  )
}