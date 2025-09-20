// // 'use client'

// // import { useState, useRef, useEffect } from 'react'
// // import { Send, Bot, User, Loader2, BarChart3, MapPin, Thermometer } from 'lucide-react'
// // import { apiClient } from '../../lib/api-client'

// // interface Message {
// //   id: string
// //   content: string
// //   sender: 'user' | 'bot'
// //   timestamp: Date
// // }

// // export default function ChatPage() {
// //   const [messages, setMessages] = useState<Message[]>([
// //     {
// //       id: '1',
// //       content: "Hello! I'm your ARGO float data assistant. I can help you explore ocean temperature, salinity, and heat content data from the Indian Ocean (2010-2013). Try asking me about temperature trends, spatial patterns, or specific measurements!",
// //       sender: 'bot',
// //       timestamp: new Date()
// //     }
// //   ])
// //   const [inputValue, setInputValue] = useState('')
// //   const [isLoading, setIsLoading] = useState(false)
// //   const messagesEndRef = useRef<HTMLDivElement>(null)
// //   const inputRef = useRef<HTMLInputElement>(null)

// //   useEffect(() => {
// //     scrollToBottom()
// //   }, [messages])

// //   const scrollToBottom = () => {
// //     messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
// //   }

// //   const handleSendMessage = async () => {
// //     if (!inputValue.trim() || isLoading) return

// //     const userMessage: Message = {
// //       id: Date.now().toString(),
// //       content: inputValue,
// //       sender: 'user',
// //       timestamp: new Date()
// //     }

// //     setMessages(prev => [...prev, userMessage])
// //     setInputValue('')
// //     setIsLoading(true)

// //     try {
// //       const response = await apiClient.chatWithData({ message: inputValue })
      
// //       const botMessage: Message = {
// //         id: (Date.now() + 1).toString(),
// //         content: response.response,
// //         sender: 'bot',
// //         timestamp: new Date()
// //       }

// //       setMessages(prev => [...prev, botMessage])
// //     } catch (error) {
// //       console.error('Chat error:', error)
      
// //       const errorMessage: Message = {
// //         id: (Date.now() + 1).toString(),
// //         content: "I apologize, but I encountered an error processing your question. Please try again or rephrase your query.",
// //         sender: 'bot',
// //         timestamp: new Date()
// //       }

// //       setMessages(prev => [...prev, errorMessage])
// //     } finally {
// //       setIsLoading(false)
// //     }
// //   }

// //   const handleKeyPress = (e: React.KeyboardEvent) => {
// //     if (e.key === 'Enter' && !e.shiftKey) {
// //       e.preventDefault()
// //       handleSendMessage()
// //     }
// //   }

// //   const suggestedQuestions = [
// //     "What is the average temperature at 60°E longitude in 2012?",
// //     "How does heat content vary between 60°E and 80°E?", 
// //     "Show me the salinity trends in the surface waters",
// //     "What are the typical temperature ranges in this dataset?"
// //   ]

// //   const handleSuggestionClick = (question: string) => {
// //     setInputValue(question)
// //     inputRef.current?.focus()
// //   }

// //   return (
// //     <div className="min-h-screen bg-gray-50 flex flex-col">
// //       {/* Header */}
// //       <header className="bg-white shadow-sm border-b">
// //         <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
// //           <div className="flex items-center justify-between py-6">
// //             <div>
// //               <h1 className="text-2xl font-bold text-gray-900">FloatChat</h1>
// //               <p className="text-gray-600 mt-1">AI assistant for ARGO float data</p>
// //             </div>
// //             <div className="flex items-center space-x-2 text-sm text-gray-500">
// //               <div className="flex items-center space-x-1">
// //                 <div className="h-2 w-2 bg-green-500 rounded-full"></div>
// //                 <span>Online</span>
// //               </div>
// //             </div>
// //           </div>
// //         </div>
// //       </header>

// //       {/* Chat Container */}
// //       <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full px-4 sm:px-6 lg:px-8">
// //         {/* Messages Area */}
// //         <div className="flex-1 py-6 overflow-hidden">
// //           <div className="h-full overflow-y-auto space-y-4 pr-2">
// //             {messages.map((message) => (
// //               <div
// //                 key={message.id}
// //                 className={`flex items-start space-x-3 ${
// //                   message.sender === 'user' ? 'justify-end' : 'justify-start'
// //                 }`}
// //               >
// //                 {message.sender === 'bot' && (
// //                   <div className="flex-shrink-0">
// //                     <div className="h-8 w-8 bg-primary-100 rounded-full flex items-center justify-center">
// //                       <Bot className="h-5 w-5 text-primary-600" />
// //                     </div>
// //                   </div>
// //                 )}
                
// //                 <div
// //                   className={`max-w-2xl px-4 py-3 rounded-lg ${
// //                     message.sender === 'user'
// //                       ? 'bg-primary-600 text-white'
// //                       : 'bg-white border shadow-sm'
// //                   }`}
// //                 >
// //                   <p className="text-sm whitespace-pre-wrap">{message.content}</p>
// //                   <div className={`text-xs mt-2 ${
// //                     message.sender === 'user' ? 'text-primary-100' : 'text-gray-500'
// //                   }`}>
// //                     {message.timestamp.toLocaleTimeString()}
// //                   </div>
// //                 </div>

// //                 {message.sender === 'user' && (
// //                   <div className="flex-shrink-0">
// //                     <div className="h-8 w-8 bg-gray-100 rounded-full flex items-center justify-center">
// //                       <User className="h-5 w-5 text-gray-600" />
// //                     </div>
// //                   </div>
// //                 )}
// //               </div>
// //             ))}
            
// //             {isLoading && (
// //               <div className="flex items-start space-x-3">
// //                 <div className="flex-shrink-0">
// //                   <div className="h-8 w-8 bg-primary-100 rounded-full flex items-center justify-center">
// //                     <Bot className="h-5 w-5 text-primary-600" />
// //                   </div>
// //                 </div>
// //                 <div className="bg-white border shadow-sm px-4 py-3 rounded-lg">
// //                   <div className="flex items-center space-x-2">
// //                     <Loader2 className="h-4 w-4 animate-spin text-primary-600" />
// //                     <span className="text-sm text-gray-600">Analyzing data...</span>
// //                   </div>
// //                 </div>
// //               </div>
// //             )}
            
// //             <div ref={messagesEndRef} />
// //           </div>
// //         </div>

// //         {/* Suggested Questions */}
// //         {messages.length === 1 && (
// //           <div className="py-4 border-t bg-white rounded-t-lg">
// //             <h3 className="text-sm font-medium text-gray-700 mb-3 px-4">Try asking about:</h3>
// //             <div className="grid grid-cols-1 md:grid-cols-2 gap-2 px-4">
// //               {suggestedQuestions.map((question, index) => (
// //                 <button
// //                   key={index}
// //                   onClick={() => handleSuggestionClick(question)}
// //                   className="text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors duration-200 text-sm border"
// //                 >
// //                   <div className="flex items-center space-x-2">
// //                     {index === 0 && <Thermometer className="h-4 w-4 text-orange-500" />}
// //                     {index === 1 && <BarChart3 className="h-4 w-4 text-blue-500" />}
// //                     {index === 2 && <MapPin className="h-4 w-4 text-green-500" />}
// //                     {index === 3 && <Bot className="h-4 w-4 text-purple-500" />}
// //                     <span className="text-gray-700">{question}</span>
// //                   </div>
// //                 </button>
// //               ))}
// //             </div>
// //           </div>
// //         )}

// //         {/* Input Area */}
// //         <div className="py-4 bg-white border-t">
// //           <div className="flex items-center space-x-3">
// //             <div className="flex-1 relative">
// //               <input
// //                 ref={inputRef}
// //                 type="text"
// //                 value={inputValue}
// //                 onChange={(e) => setInputValue(e.target.value)}
// //                 onKeyPress={handleKeyPress}
// //                 placeholder="Ask about ocean temperature, salinity, or heat content..."
// //                 className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
// //                 disabled={isLoading}
// //               />
// //             </div>
// //             <button
// //               onClick={handleSendMessage}
// //               disabled={!inputValue.trim() || isLoading}
// //               className="btn-primary p-3 disabled:opacity-50 disabled:cursor-not-allowed"
// //             >
// //               <Send className="h-5 w-5" />
// //             </button>
// //           </div>
          
// //           <div className="mt-2 text-xs text-gray-500 px-4">
// //             Press Enter to send, Shift+Enter for new line
// //           </div>
// //         </div>
// //       </div>
// //     </div>
// //   )
// // }


// // 'use client'

// // import { useState, useRef, useEffect } from 'react'
// // import { Send, Bot, User, Loader2, BarChart3, MapPin, Thermometer, Upload, HardDriveDownload, Info } from 'lucide-react'
// // import { apiClient, APIError } from '../../lib/api-client'

// // type Sender = 'user' | 'bot' | 'system'

// // interface Message {
// //   id: string
// //   content: string
// //   sender: Sender
// //   timestamp: Date
// // }

// // export default function ChatPage() {
// //   const [messages, setMessages] = useState<Message[]>([
// //     {
// //       id: 'welcome',
// //       content:
// //         "Hello! I'm your ARGO data assistant. Ingest a NetCDF (e.g., tempsal.nc) to ground responses, or ask about temperature, salinity, and heat content in the Indian Ocean (2010–2013).",
// //       sender: 'system',
// //       timestamp: new Date(),
// //     },
// //   ])
// //   const [inputValue, setInputValue] = useState('')
// //   const [isLoading, setIsLoading] = useState(false)

// //   // Active dataset context from ingestion
// //   const [datasetCtx, setDatasetCtx] = useState<Record<string, any> | null>(null)
// //   const [pathInput, setPathInput] = useState('')

// //   const fileInputRef = useRef<HTMLInputElement | null>(null)
// //   const messagesEndRef = useRef<HTMLDivElement>(null)
// //   const inputRef = useRef<HTMLInputElement>(null)

// //   useEffect(() => {
// //     messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
// //   }, [messages])

// //   const handleSendMessage = async () => {
// //     if (!inputValue.trim() || isLoading) return

// //     const userMessage: Message = {
// //       id: crypto.randomUUID(),
// //       content: inputValue,
// //       sender: 'user',
// //       timestamp: new Date(),
// //     }
// //     setMessages(prev => [...prev, userMessage])
// //     setInputValue('')
// //     setIsLoading(true)

// //     try {
// //       const resp = await apiClient.chatWithData({
// //         message: userMessage.content,
// //         context: datasetCtx || undefined,
// //       })
// //       const botMessage: Message = {
// //         id: crypto.randomUUID(),
// //         content: resp.response,
// //         sender: 'bot',
// //         timestamp: new Date(resp.timestamp || Date.now()),
// //       }
// //       setMessages(prev => [...prev, botMessage])
// //     } catch (error) {
// //       const msg =
// //         error instanceof APIError ? error.message : 'An error occurred while processing the question.'
// //       setMessages(prev => [
// //         ...prev,
// //         { id: crypto.randomUUID(), content: `Error: ${msg}`, sender: 'system', timestamp: new Date() },
// //       ])
// //     } finally {
// //       setIsLoading(false)
// //     }
// //   }

// //   const handleKeyPress = (e: React.KeyboardEvent) => {
// //     if (e.key === 'Enter' && !e.shiftKey) {
// //       e.preventDefault()
// //       handleSendMessage()
// //     }
// //   }

// //   // Ingest via upload
// //   const onChooseFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
// //     const f = e.target.files?.[0]
// //     if (!f) return
// //     setMessages(prev => [
// //       ...prev,
// //       { id: crypto.randomUUID(), content: `Uploading ${f.name} for ingestion...`, sender: 'system', timestamp: new Date() },
// //     ])
// //     try {
// //       const res = await apiClient.ingestNetcdfUpload(f)
// //       setDatasetCtx({
// //         parquet_path: res.output_file,
// //         date_range: res.metadata?.date_range,
// //         spatial_bounds: res.metadata?.spatial_bounds,
// //         variables: res.metadata?.variables,
// //         dims: res.metadata?.dims,
// //       })
// //       setMessages(prev => [
// //         ...prev,
// //         {
// //           id: crypto.randomUUID(),
// //           content: `Dataset ingested (${res.records} rows).\nParquet: ${res.output_file}\nTime: ${JSON.stringify(
// //             res.metadata?.date_range
// //           )}\nBounds: ${JSON.stringify(res.metadata?.spatial_bounds)}`,
// //           sender: 'system',
// //           timestamp: new Date(),
// //         },
// //       ])
// //     } catch (error) {
// //       const msg = error instanceof APIError ? error.message : String(error)
// //       setMessages(prev => [
// //         ...prev,
// //         { id: crypto.randomUUID(), content: `Ingestion failed: ${msg}`, sender: 'system', timestamp: new Date() },
// //       ])
// //     } finally {
// //       if (fileInputRef.current) fileInputRef.current.value = ''
// //     }
// //   }

// //   // Ingest via server-side path
// //   const onIngestPath = async () => {
// //     const p = pathInput.trim()
// //     if (!p) return
// //     setMessages(prev => [
// //       ...prev,
// //       { id: crypto.randomUUID(), content: `Ingesting from path: ${p}`, sender: 'system', timestamp: new Date() },
// //     ])
// //     try {
// //       const res = await apiClient.ingestNetcdfByPath(p)
// //       setDatasetCtx({
// //         parquet_path: res.output_file,
// //         date_range: res.metadata?.date_range,
// //         spatial_bounds: res.metadata?.spatial_bounds,
// //         variables: res.metadata?.variables,
// //         dims: res.metadata?.dims,
// //       })
// //       setMessages(prev => [
// //         ...prev,
// //         {
// //           id: crypto.randomUUID(),
// //           content: `Dataset ingested (${res.records} rows).\nParquet: ${res.output_file}\nTime: ${JSON.stringify(
// //             res.metadata?.date_range
// //           )}\nBounds: ${JSON.stringify(res.metadata?.spatial_bounds)}`,
// //           sender: 'system',
// //           timestamp: new Date(),
// //         },
// //       ])
// //     } catch (error) {
// //       const msg = error instanceof APIError ? error.message : String(error)
// //       setMessages(prev => [
// //         ...prev,
// //         { id: crypto.randomUUID(), content: `Ingestion failed: ${msg}`, sender: 'system', timestamp: new Date() },
// //       ])
// //     }
// //   }

// //   const suggestedQuestions = [
// //     'What is the average temperature at 60°E longitude in 2012?',
// //     'How does heat content vary between 60°E and 80°E?',
// //     'Show me the salinity trends in the surface waters',
// //     'What are the typical temperature ranges in this dataset?',
// //   ]

// //   const handleSuggestionClick = (question: string) => {
// //     setInputValue(question)
// //     inputRef.current?.focus()
// //   }

// //   return (
// //     <div className="min-h-screen bg-gray-50 flex flex-col">
// //       {/* Header */}
// //       <header className="bg-white shadow-sm border-b">
// //         <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
// //           <div className="flex items-center justify-between py-6">
// //             <div>
// //               <h1 className="text-2xl font-bold text-gray-900">FloatChat</h1>
// //               <p className="text-gray-600 mt-1">AI assistant for ARGO float and gridded data</p>
// //             </div>
// //             <div className="flex items-center space-x-2 text-sm text-gray-500">
// //               <div className="flex items-center space-x-1">
// //                 <div className="h-2 w-2 bg-green-500 rounded-full" />
// //                 <span>Online</span>
// //               </div>
// //             </div>
// //           </div>
// //         </div>
// //       </header>

// //       {/* Body */}
// //       <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full px-4 sm:px-6 lg:px-8">
// //         {/* Ingestion Controls */}
// //         <div className="mt-4 rounded-md border bg-white p-3 space-y-2">
// //           <div className="flex items-center gap-2 text-sm text-gray-600">
// //             <Info size={16} /> Ingest a NetCDF to ground the chat on the active dataset.
// //           </div>
// //           <div className="flex flex-wrap items-center gap-2">
// //             <input ref={fileInputRef} type="file" accept=".nc" onChange={onChooseFile} className="hidden" />
// //             <button
// //               onClick={() => fileInputRef.current?.click()}
// //               className="inline-flex items-center gap-2 rounded-md bg-blue-600 px-3 py-1.5 text-white"
// //             >
// //               <Upload size={16} /> Upload .nc
// //             </button>
// //             <div className="flex items-center gap-2">
// //               <input
// //                 value={pathInput}
// //                 onChange={e => setPathInput(e.target.value)}
// //                 placeholder="Server path e.g. netcdf_data/tempsal.nc"
// //                 className="w-80 rounded-md border px-2 py-1"
// //               />
// //               <button
// //                 onClick={onIngestPath}
// //                 className="inline-flex items-center gap-2 rounded-md bg-slate-700 px-3 py-1.5 text-white"
// //               >
// //                 <HardDriveDownload size={16} /> Ingest Path
// //               </button>
// //             </div>
// //           </div>
// //           {datasetCtx && (
// //             <div className="text-xs text-gray-600">
// //               ActiveDataset → {datasetCtx.parquet_path} • Time {JSON.stringify(datasetCtx.date_range)} • Bounds{' '}
// //               {JSON.stringify(datasetCtx.spatial_bounds)}
// //             </div>
// //           )}
// //         </div>

// //         {/* Messages */}
// //         <div className="flex-1 py-6 overflow-hidden">
// //           <div className="h-full overflow-y-auto space-y-4 pr-2">
// //             {messages.map(message => (
// //               <div
// //                 key={message.id}
// //                 className={`flex items-start space-x-3 ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
// //               >
// //                 {message.sender !== 'user' && (
// //                   <div className="flex-shrink-0">
// //                     <div className="h-8 w-8 bg-primary-100 rounded-full flex items-center justify-center">
// //                       <Bot className="h-5 w-5 text-primary-600" />
// //                     </div>
// //                   </div>
// //                 )}

// //                 <div
// //                   className={`max-w-2xl px-4 py-3 rounded-lg ${
// //                     message.sender === 'user' ? 'bg-primary-600 text-white' : 'bg-white border shadow-sm'
// //                   }`}
// //                 >
// //                   <p className="text-sm whitespace-pre-wrap">{message.content}</p>
// //                   <div
// //                     className={`text-xs mt-2 ${
// //                       message.sender === 'user' ? 'text-primary-100' : 'text-gray-500'
// //                     }`}
// //                   >
// //                     {message.timestamp.toLocaleTimeString()}
// //                   </div>
// //                 </div>

// //                 {message.sender === 'user' && (
// //                   <div className="flex-shrink-0">
// //                     <div className="h-8 w-8 bg-gray-100 rounded-full flex items-center justify-center">
// //                       <User className="h-5 w-5 text-gray-600" />
// //                     </div>
// //                   </div>
// //                 )}
// //               </div>
// //             ))}

// //             {isLoading && (
// //               <div className="flex items-start space-x-3">
// //                 <div className="flex-shrink-0">
// //                   <div className="h-8 w-8 bg-primary-100 rounded-full flex items-center justify-center">
// //                     <Bot className="h-5 w-5 text-primary-600" />
// //                   </div>
// //                 </div>
// //                 <div className="bg-white border shadow-sm px-4 py-3 rounded-lg">
// //                   <div className="flex items-center space-x-2">
// //                     <Loader2 className="h-4 w-4 animate-spin text-primary-600" />
// //                     <span className="text-sm text-gray-600">Analyzing data...</span>
// //                   </div>
// //                 </div>
// //               </div>
// //             )}

// //             <div ref={messagesEndRef} />
// //           </div>
// //         </div>

// //         {/* Suggested Questions */}
// //         {messages.length <= 2 && (
// //           <div className="py-4 border-t bg-white rounded-t-lg">
// //             <h3 className="text-sm font-medium text-gray-700 mb-3 px-4">Try asking about:</h3>
// //             <div className="grid grid-cols-1 md:grid-cols-2 gap-2 px-4">
// //               {suggestedQuestions.map((question, index) => (
// //                 <button
// //                   key={index}
// //                   onClick={() => handleSuggestionClick(question)}
// //                   className="text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors duration-200 text-sm border"
// //                 >
// //                   <div className="flex items-center space-x-2">
// //                     {index === 0 && <Thermometer className="h-4 w-4 text-orange-500" />}
// //                     {index === 1 && <BarChart3 className="h-4 w-4 text-blue-500" />}
// //                     {index === 2 && <MapPin className="h-4 w-4 text-green-500" />}
// //                     {index === 3 && <Bot className="h-4 w-4 text-purple-500" />}
// //                     <span className="text-gray-700">{question}</span>
// //                   </div>
// //                 </button>
// //               ))}
// //             </div>
// //           </div>
// //         )}

// //         {/* Composer */}
// //         <div className="py-4 bg-white border-t">
// //           <div className="flex items-center space-x-3">
// //             <div className="flex-1 relative">
// //               <input
// //                 ref={inputRef}
// //                 type="text"
// //                 value={inputValue}
// //                 onChange={e => setInputValue(e.target.value)}
// //                 onKeyDown={handleKeyPress}
// //                 placeholder="Ask about ocean temperature, salinity, or heat content..."
// //                 className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
// //                 disabled={isLoading}
// //               />
// //             </div>
// //             <button
// //               onClick={handleSendMessage}
// //               disabled={!inputValue.trim() || isLoading}
// //               className="btn-primary p-3 disabled:opacity-50 disabled:cursor-not-allowed"
// //             >
// //               <Send className="h-5 w-5" />
// //             </button>
// //           </div>
// //           <div className="mt-2 text-xs text-gray-500 px-4">Press Enter to send, Shift+Enter for new line</div>
// //         </div>
// //       </div>
// //     </div>
// //   )
// // }



// 'use client'

// import { useState, useRef, useEffect } from 'react'
// import { Send, Bot, User, Loader2, BarChart3, MapPin, Thermometer, Upload, HardDriveDownload, Info } from 'lucide-react'
// import { apiClient, APIError } from '../../lib/api-client'

// type Sender = 'user' | 'bot' | 'system'

// interface Message {
//   id: string
//   content: string
//   sender: Sender
//   timestamp: Date
//   tsStr: string // preformatted, stable at creation time
// }

// export default function ChatPage() {
//   const [mounted, setMounted] = useState(false)
//   useEffect(() => setMounted(true), [])

//   const [messages, setMessages] = useState<Message[]>([
//     {
//       id: 'welcome',
//       content:
//         "Hello! I'm your ARGO data assistant. Ingest a NetCDF (e.g., tempsal.nc) to ground responses, or ask about temperature, salinity, and heat content in the Indian Ocean (2010–2013).",
//       sender: 'system',
//       timestamp: new Date(),
//       tsStr: new Date().toLocaleTimeString(),
//     },
//   ])
//   const [inputValue, setInputValue] = useState('')
//   const [isLoading, setIsLoading] = useState(false)

//   // Active dataset context from ingestion
//   const [datasetCtx, setDatasetCtx] = useState<Record<string, any> | null>(null)
//   const [pathInput, setPathInput] = useState('')

//   const fileInputRef = useRef<HTMLInputElement | null>(null)
//   const messagesEndRef = useRef<HTMLDivElement>(null)
//   const inputRef = useRef<HTMLInputElement>(null)

//   useEffect(() => {
//     messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
//   }, [messages])

//   const handleSendMessage = async () => {
//     if (!inputValue.trim() || isLoading) return

//     const now = new Date()
//     const userMessage: Message = {
//       id: crypto.randomUUID(),
//       content: inputValue,
//       sender: 'user',
//       timestamp: now,
//       tsStr: now.toLocaleTimeString(),
//     }
//     setMessages(prev => [...prev, userMessage])
//     setInputValue('')
//     setIsLoading(true)

//     try {
//       const resp = await apiClient.chatWithData({
//         message: userMessage.content,
//         context: datasetCtx || undefined,
//       })
//       const botTs = resp.timestamp ? new Date(resp.timestamp) : new Date()
//       const botMessage: Message = {
//         id: crypto.randomUUID(),
//         content: resp.response,
//         sender: 'bot',
//         timestamp: botTs,
//         tsStr: botTs.toLocaleTimeString(),
//       }
//       setMessages(prev => [...prev, botMessage])
//     } catch (error) {
//       const msg = error instanceof APIError ? error.message : 'An error occurred while processing the question.'
//       const errNow = new Date()
//       setMessages(prev => [
//         ...prev,
//         { id: crypto.randomUUID(), content: `Error: ${msg}`, sender: 'system', timestamp: errNow, tsStr: errNow.toLocaleTimeString() },
//       ])
//     } finally {
//       setIsLoading(false)
//     }
//   }

//   const handleKeyPress = (e: React.KeyboardEvent) => {
//     if (e.key === 'Enter' && !e.shiftKey) {
//       e.preventDefault()
//       handleSendMessage()
//     }
//   }

//   // Ingest via upload
//   const onChooseFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
//     const f = e.target.files?.[0]
//     if (!f) return
//     const now = new Date()
//     setMessages(prev => [
//       ...prev,
//       { id: crypto.randomUUID(), content: `Uploading ${f.name} for ingestion...`, sender: 'system', timestamp: now, tsStr: now.toLocaleTimeString() },
//     ])
//     try {
//       const res = await apiClient.ingestNetcdfUpload(f)
//       setDatasetCtx({
//         parquet_path: res.output_file,
//         date_range: res.metadata?.date_range,
//         spatial_bounds: res.metadata?.spatial_bounds,
//         variables: res.metadata?.variables,
//         dims: res.metadata?.dims,
//       })
//       const n = new Date()
//       setMessages(prev => [
//         ...prev,
//         {
//           id: crypto.randomUUID(),
//           content: `Dataset ingested (${res.records} rows).\nParquet: ${res.output_file}\nTime: ${JSON.stringify(
//             res.metadata?.date_range
//           )}\nBounds: ${JSON.stringify(res.metadata?.spatial_bounds)}`,
//           sender: 'system',
//           timestamp: n,
//           tsStr: n.toLocaleTimeString(),
//         },
//       ])
//     } catch (error) {
//       const n = new Date()
//       const msg = error instanceof APIError ? error.message : String(error)
//       setMessages(prev => [
//         ...prev,
//         { id: crypto.randomUUID(), content: `Ingestion failed: ${msg}`, sender: 'system', timestamp: n, tsStr: n.toLocaleTimeString() },
//       ])
//     } finally {
//       if (fileInputRef.current) fileInputRef.current.value = ''
//     }
//   }

//   // Ingest via server-side path
//   const onIngestPath = async () => {
//     const p = pathInput.trim()
//     if (!p) return
//     const now = new Date()
//     setMessages(prev => [
//       ...prev,
//       { id: crypto.randomUUID(), content: `Ingesting from path: ${p}`, sender: 'system', timestamp: now, tsStr: now.toLocaleTimeString() },
//     ])
//     try {
//       const res = await apiClient.ingestNetcdfByPath(p)
//       setDatasetCtx({
//         parquet_path: res.output_file,
//         date_range: res.metadata?.date_range,
//         spatial_bounds: res.metadata?.spatial_bounds,
//         variables: res.metadata?.variables,
//         dims: res.metadata?.dims,
//       })
//       const n = new Date()
//       setMessages(prev => [
//         ...prev,
//         {
//           id: crypto.randomUUID(),
//           content: `Dataset ingested (${res.records} rows).\nParquet: ${res.output_file}\nTime: ${JSON.stringify(
//             res.metadata?.date_range
//           )}\nBounds: ${JSON.stringify(res.metadata?.spatial_bounds)}`,
//           sender: 'system',
//           timestamp: n,
//           tsStr: n.toLocaleTimeString(),
//         },
//       ])
//     } catch (error) {
//       const n = new Date()
//       const msg = error instanceof APIError ? error.message : String(error)
//       setMessages(prev => [
//         ...prev,
//         { id: crypto.randomUUID(), content: `Ingestion failed: ${msg}`, sender: 'system', timestamp: n, tsStr: n.toLocaleTimeString() },
//       ])
//     }
//   }

//   const suggestedQuestions = [
//     'What is the average temperature at 60°E longitude in 2012?',
//     'How does heat content vary between 60°E and 80°E?',
//     'Show me the salinity trends in the surface waters',
//     'What are the typical temperature ranges in this dataset?',
//   ]

//   const handleSuggestionClick = (question: string) => {
//     setInputValue(question)
//     inputRef.current?.focus()
//   }

//   return (
//     <div className="min-h-screen bg-gray-50 flex flex-col">
//       {/* Header */}
//       <header className="bg-white shadow-sm border-b">
//         <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
//           <div className="flex items-center justify-between py-6">
//             <div>
//               <h1 className="text-2xl font-bold text-gray-900">FloatChat</h1>
//               <p className="text-gray-600 mt-1">AI assistant for ARGO float and gridded data</p>
//             </div>
//             <div className="flex items-center space-x-2 text-sm text-gray-500">
//               <div className="flex items-center space-x-1">
//                 <div className="h-2 w-2 bg-green-500 rounded-full" />
//                 <span>Online</span>
//               </div>
//             </div>
//           </div>
//         </div>
//       </header>

//       {/* Body */}
//       <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full px-4 sm:px-6 lg:px-8">
//         {/* Ingestion Controls */}
//         <div className="mt-4 rounded-md border bg-white p-3 space-y-2">
//           <div className="flex items-center gap-2 text-sm text-gray-600">
//             <Info size={16} /> Ingest a NetCDF to ground the chat on the active dataset.
//           </div>
//           <div className="flex flex-wrap items-center gap-2">
//             <input ref={fileInputRef} type="file" accept=".nc" onChange={onChooseFile} className="hidden" />
//             <button
//               onClick={() => fileInputRef.current?.click()}
//               className="inline-flex items-center gap-2 rounded-md bg-blue-600 px-3 py-1.5 text-white"
//             >
//               <Upload size={16} /> Upload .nc
//             </button>
//             <div className="flex items-center gap-2">
//               <input
//                 value={pathInput}
//                 onChange={e => setPathInput(e.target.value)}
//                 placeholder="Server path e.g. netcdf_data/tempsal.nc"
//                 className="w-80 rounded-md border px-2 py-1"
//               />
//               <button
//                 onClick={onIngestPath}
//                 className="inline-flex items-center gap-2 rounded-md bg-slate-700 px-3 py-1.5 text-white"
//               >
//                 <HardDriveDownload size={16} /> Ingest Path
//               </button>
//             </div>
//           </div>
//           {datasetCtx && (
//             <div className="text-xs text-gray-600">
//               ActiveDataset → {datasetCtx.parquet_path} • Time {JSON.stringify(datasetCtx.date_range)} • Bounds{' '}
//               {JSON.stringify(datasetCtx.spatial_bounds)}
//             </div>
//           )}
//         </div>

//         {/* Messages */}
//         <div className="flex-1 py-6 overflow-hidden">
//           <div className="h-full overflow-y-auto space-y-4 pr-2">
//             {messages.map(message => (
//               <div
//                 key={message.id}
//                 className={`flex items-start space-x-3 ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
//               >
//                 {message.sender !== 'user' && (
//                   <div className="flex-shrink-0">
//                     <div className="h-8 w-8 bg-primary-100 rounded-full flex items-center justify-center">
//                       <Bot className="h-5 w-5 text-primary-600" />
//                     </div>
//                   </div>
//                 )}

//                 <div
//                   className={`max-w-2xl px-4 py-3 rounded-lg ${
//                     message.sender === 'user' ? 'bg-primary-600 text-white' : 'bg-white border shadow-sm'
//                   }`}
//                 >
//                   <p className="text-sm whitespace-pre-wrap">{message.content}</p>
//                   <div className={`text-xs mt-2 ${message.sender === 'user' ? 'text-primary-100' : 'text-gray-500'}`}>
//                     {/* Render only after mount to avoid SSR/CSR mismatch; use stable tsStr */}
//                     {mounted ? message.tsStr : ''}
//                   </div>
//                 </div>

//                 {message.sender === 'user' && (
//                   <div className="flex-shrink-0">
//                     <div className="h-8 w-8 bg-gray-100 rounded-full flex items-center justify-center">
//                       <User className="h-5 w-5 text-gray-600" />
//                     </div>
//                   </div>
//                 )}
//               </div>
//             ))}

//             {isLoading && (
//               <div className="flex items-start space-x-3">
//                 <div className="flex-shrink-0">
//                   <div className="h-8 w-8 bg-primary-100 rounded-full flex items-center justify-center">
//                     <Bot className="h-5 w-5 text-primary-600" />
//                   </div>
//                 </div>
//                 <div className="bg-white border shadow-sm px-4 py-3 rounded-lg">
//                   <div className="flex items-center space-x-2">
//                     <Loader2 className="h-4 w-4 animate-spin text-primary-600" />
//                     <span className="text-sm text-gray-600">Analyzing data...</span>
//                   </div>
//                 </div>
//               </div>
//             )}

//             <div ref={messagesEndRef} />
//           </div>
//         </div>

//         {/* Suggested Questions */}
//         {messages.length <= 2 && (
//           <div className="py-4 border-t bg-white rounded-t-lg">
//             <h3 className="text-sm font-medium text-gray-700 mb-3 px-4">Try asking about:</h3>
//             <div className="grid grid-cols-1 md:grid-cols-2 gap-2 px-4">
//               {[
//                 'What is the average temperature at 60°E longitude in 2012?',
//                 'How does heat content vary between 60°E and 80°E?',
//                 'Show me the salinity trends in the surface waters',
//                 'What are the typical temperature ranges in this dataset?',
//               ].map((question, index) => (
//                 <button
//                   key={index}
//                   onClick={() => {
//                     setInputValue(question)
//                     inputRef.current?.focus()
//                   }}
//                   className="text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors duration-200 text-sm border"
//                 >
//                   <div className="flex items-center space-x-2">
//                     {index === 0 && <Thermometer className="h-4 w-4 text-orange-500" />}
//                     {index === 1 && <BarChart3 className="h-4 w-4 text-blue-500" />}
//                     {index === 2 && <MapPin className="h-4 w-4 text-green-500" />}
//                     {index === 3 && <Bot className="h-4 w-4 text-purple-500" />}
//                     <span className="text-gray-700">{question}</span>
//                   </div>
//                 </button>
//               ))}
//             </div>
//           </div>
//         )}

//         {/* Composer */}
//         <div className="py-4 bg-white border-t">
//           <div className="flex items-center space-x-3">
//             <div className="flex-1 relative">
//               <input
//                 ref={inputRef}
//                 type="text"
//                 value={inputValue}
//                 onChange={e => setInputValue(e.target.value)}
//                 onKeyDown={handleKeyPress}
//                 placeholder="Ask about ocean temperature, salinity, or heat content..."
//                 className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
//                 disabled={isLoading}
//               />
//             </div>
//             <button
//               onClick={handleSendMessage}
//               disabled={!inputValue.trim() || isLoading}
//               className="btn-primary p-3 disabled:opacity-50 disabled:cursor-not-allowed"
//             >
//               <Send className="h-5 w-5" />
//             </button>
//           </div>
//           <div className="mt-2 text-xs text-gray-500 px-4">Press Enter to send, Shift+Enter for new line</div>
//         </div>
//       </div>
//     </div>
//   )
// }



'use client'

import { useState, useRef, useEffect } from 'react'
import {
  Send, Bot, User, Loader2, BarChart3, MapPin, Thermometer,
  Upload, HardDriveDownload, Info
} from 'lucide-react'
import {
  apiClient, APIError,
  type TimeSeriesPoint, type VerticalProfilePoint, type HeatContentPoint
} from '../../lib/api-client'
import { TimeSeriesChart } from '../../components/charts/TimeSeriesChart'
import { VerticalProfileChart } from '../../components/charts/VerticalProfileChart'
import { HeatmapChart } from '../../components/charts/HeatmapChart'

// ---------- Helpers ----------
type Sender = 'user' | 'bot' | 'system'

interface Message {
  id: string
  content: string
  sender: Sender
  timestamp: Date
  tsStr: string // stable preformatted time string to avoid hydration mismatches
}

function chooseVizIntent(text: string): 'ts' | 'profile' | 'heat' {
  const s = text.toLowerCase()
  if (s.includes('heat content') || s.includes('heatmap')) return 'heat'
  if (s.includes('profile') || s.includes('depth')) return 'profile'
  return 'ts'
}

// Inline viz widget
function ChatViz({
  datasetCtx,
  initialViz,
  initLat,
  initLon,
  initStart,
  initEnd,
  initProfileDate = '2012-06-15',
}: {
  datasetCtx: Record<string, any>
  initialViz: 'ts' | 'profile' | 'heat'
  initLat: number
  initLon: number
  initStart: string
  initEnd: string
  initProfileDate?: string
}) {
  const [viz, setViz] = useState<'ts' | 'profile' | 'heat'>(initialViz)
  const [lat, setLat] = useState<number>(initLat)
  const [lon, setLon] = useState<number>(initLon)
  const [start, setStart] = useState<string>(initStart)
  const [end, setEnd] = useState<string>(initEnd)
  const [profileDate, setProfileDate] = useState<string>(initProfileDate)

  const [tsData, setTsData] = useState<TimeSeriesPoint[]>([])
  const [pfData, setPfData] = useState<VerticalProfilePoint[]>([])
  const [hcData, setHcData] = useState<HeatContentPoint[]>([])
  const [loading, setLoading] = useState<boolean>(false)

  async function fetchData() {
    setLoading(true)
    try {
      if (viz === 'ts') {
        const d = await apiClient.getSurfaceTimeseries({ lat, lon, start, end })
        setTsData(d)
      } else if (viz === 'profile') {
        const d = await apiClient.getVerticalProfile({ lat, lon, date: profileDate })
        setPfData(d)
      } else {
        const d = await apiClient.getHeatContent({ lat, lon, start, end })
        setHcData(d)
      }
    } catch (e) {
      console.error('Viz fetch failed:', e)
      setTsData([]); setPfData([]); setHcData([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchData() }, [viz])

  return (
    <div className="mt-2 rounded-md border bg-white p-3">
      <div className="flex flex-wrap items-center gap-2 mb-2 text-xs">
        <div className="flex items-center gap-1">
          <span>Lat</span>
          <input className="w-20 rounded border px-1 py-0.5" type="number" step="0.1"
            value={isNaN(lat) ? '' : lat} onChange={e => setLat(parseFloat(e.target.value))} />
        </div>
        <div className="flex items-center gap-1">
          <span>Lon</span>
          <input className="w-20 rounded border px-1 py-0.5" type="number" step="0.1"
            value={isNaN(lon) ? '' : lon} onChange={e => setLon(parseFloat(e.target.value))} />
        </div>

        {viz !== 'profile' ? (
          <>
            <div className="flex items-center gap-1">
              <span>Start</span>
              <input className="rounded border px-1 py-0.5" type="date"
                value={start} onChange={e => setStart(e.target.value)} />
            </div>
            <div className="flex items-center gap-1">
              <span>End</span>
              <input className="rounded border px-1 py-0.5" type="date"
                value={end} onChange={e => setEnd(e.target.value)} />
            </div>
          </>
        ) : (
          <div className="flex items-center gap-1">
            <span>Date</span>
            <input className="rounded border px-1 py-0.5" type="date"
              value={profileDate} onChange={e => setProfileDate(e.target.value)} />
          </div>
        )}

        <button onClick={fetchData} className="ml-2 rounded bg-slate-700 px-2 py-1 text-white">Update</button>

        <div className="ml-auto flex items-center gap-1">
          <button onClick={() => setViz('ts')}
            className={`rounded px-2 py-1 ${viz === 'ts' ? 'bg-blue-600 text-white' : 'bg-gray-100'}`}>TS</button>
          <button onClick={() => setViz('profile')}
            className={`rounded px-2 py-1 ${viz === 'profile' ? 'bg-blue-600 text-white' : 'bg-gray-100'}`}>Prof</button>
          <button onClick={() => setViz('heat')}
            className={`rounded px-2 py-1 ${viz === 'heat' ? 'bg-blue-600 text-white' : 'bg-gray-100'}`}>Heat</button>
        </div>
      </div>

      <div className="h-64">
        {viz === 'ts' && <TimeSeriesChart data={tsData} loading={loading} height={240} />}
        {viz === 'profile' && <VerticalProfileChart data={pfData} loading={loading} height={240} />}
        {viz === 'heat' && <HeatmapChart data={hcData} loading={loading} height={240} />}
      </div>
    </div>
  )
}

// ---------- Chat Page ----------
export default function ChatPage() {
  // Hydration-safe rendering for timestamp text
  const [mounted, setMounted] = useState(false)
  useEffect(() => setMounted(true), [])

  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      content:
        "Hello! I'm your ARGO data assistant. Ingest a NetCDF (e.g., tempsal.nc) to ground responses, or ask about temperature, salinity, and heat content in the Indian Ocean (2010–2013).",
      sender: 'system',
      timestamp: new Date(),
      tsStr: new Date().toLocaleTimeString(),
    },
  ])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  // Active dataset context from ingestion
  const [datasetCtx, setDatasetCtx] = useState<Record<string, any> | null>(null)
  const [pathInput, setPathInput] = useState('')

  const fileInputRef = useRef<HTMLInputElement | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return
    const now = new Date()
    const userMessage: Message = {
      id: crypto.randomUUID(),
      content: inputValue,
      sender: 'user',
      timestamp: now,
      tsStr: now.toLocaleTimeString(),
    }
    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsLoading(true)

    try {
      const resp = await apiClient.chatWithData({
        message: userMessage.content,
        context: datasetCtx || undefined,
      })
      const botTs = resp.timestamp ? new Date(resp.timestamp) : new Date()
      const botMessage: Message = {
        id: crypto.randomUUID(),
        content: resp.response,
        sender: 'bot',
        timestamp: botTs,
        tsStr: botTs.toLocaleTimeString(),
      }
      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      const msg = error instanceof APIError ? error.message : 'An error occurred while processing the question.'
      const n = new Date()
      setMessages(prev => [
        ...prev,
        { id: crypto.randomUUID(), content: `Error: ${msg}`, sender: 'system', timestamp: n, tsStr: n.toLocaleTimeString() },
      ])
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

  // Ingest via upload
  const onChooseFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0]
    if (!f) return
    const now = new Date()
    setMessages(prev => [
      ...prev,
      { id: crypto.randomUUID(), content: `Uploading ${f.name} for ingestion...`, sender: 'system', timestamp: now, tsStr: now.toLocaleTimeString() },
    ])
    try {
      const res = await apiClient.ingestNetcdfUpload(f)
      setDatasetCtx({
        parquet_path: res.output_file,
        date_range: res.metadata?.date_range,
        spatial_bounds: res.metadata?.spatial_bounds,
        variables: res.metadata?.variables,
        dims: res.metadata?.dims,
      })
      const n = new Date()
      setMessages(prev => [
        ...prev,
        {
          id: crypto.randomUUID(),
          content: `Dataset ingested (${res.records} rows).\nParquet: ${res.output_file}\nTime: ${JSON.stringify(
            res.metadata?.date_range
          )}\nBounds: ${JSON.stringify(res.metadata?.spatial_bounds)}`,
          sender: 'system',
          timestamp: n,
          tsStr: n.toLocaleTimeString(),
        },
      ])
    } catch (error) {
      const n = new Date()
      const msg = error instanceof APIError ? error.message : String(error)
      setMessages(prev => [
        ...prev,
        { id: crypto.randomUUID(), content: `Ingestion failed: ${msg}`, sender: 'system', timestamp: n, tsStr: n.toLocaleTimeString() },
      ])
    } finally {
      if (fileInputRef.current) fileInputRef.current.value = ''
    }
  }

  // Ingest via server-side path
  const onIngestPath = async () => {
    const p = pathInput.trim()
    if (!p) return
    const now = new Date()
    setMessages(prev => [
      ...prev,
      { id: crypto.randomUUID(), content: `Ingesting from path: ${p}`, sender: 'system', timestamp: now, tsStr: now.toLocaleTimeString() },
    ])
    try {
      const res = await apiClient.ingestNetcdfByPath(p)
      setDatasetCtx({
        parquet_path: res.output_file,
        date_range: res.metadata?.date_range,
        spatial_bounds: res.metadata?.spatial_bounds,
        variables: res.metadata?.variables,
        dims: res.metadata?.dims,
      })
      const n = new Date()
      setMessages(prev => [
        ...prev,
        {
          id: crypto.randomUUID(),
          content: `Dataset ingested (${res.records} rows).\nParquet: ${res.output_file}\nTime: ${JSON.stringify(
            res.metadata?.date_range
          )}\nBounds: ${JSON.stringify(res.metadata?.spatial_bounds)}`,
          sender: 'system',
          timestamp: n,
          tsStr: n.toLocaleTimeString(),
        },
      ])
    } catch (error) {
      const n = new Date()
      const msg = error instanceof APIError ? error.message : String(error)
      setMessages(prev => [
        ...prev,
        { id: crypto.randomUUID(), content: `Ingestion failed: ${msg}`, sender: 'system', timestamp: n, tsStr: n.toLocaleTimeString() },
      ])
    }
  }

  const suggestedQuestions = [
    'What is the average temperature at 60°E longitude in 2012?',
    'How does heat content vary between 60°E and 80°E?',
    'Show me the salinity trends in the surface waters',
    'What are the typical temperature ranges in this dataset?',
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
              <p className="text-gray-600 mt-1">AI assistant for ARGO float and gridded data</p>
            </div>
            <div className="flex items-center space-x-2 text-sm text-gray-500">
              <div className="flex items-center space-x-1">
                <div className="h-2 w-2 bg-green-500 rounded-full" />
                <span>Online</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Body */}
      <div className="flex-1 flex flex-col max-w-4xl mx-auto w-full px-4 sm:px-6 lg:px-8">
        {/* Ingestion Controls */}
        <div className="mt-4 rounded-md border bg-white p-3 space-y-2">
          <div className="flex items-center gap-2 text-sm text-gray-600">
            <Info size={16} /> Ingest a NetCDF to ground the chat on the active dataset.
          </div>
          <div className="flex flex-wrap items-center gap-2">
            <input ref={fileInputRef} type="file" accept=".nc" onChange={onChooseFile} className="hidden" />
            <button
              onClick={() => fileInputRef.current?.click()}
              className="inline-flex items-center gap-2 rounded-md bg-blue-600 px-3 py-1.5 text-white"
            >
              <Upload size={16} /> Upload .nc
            </button>
            <div className="flex items-center gap-2">
              <input
                value={pathInput}
                onChange={e => setPathInput(e.target.value)}
                placeholder="Server path e.g. netcdf_data/tempsal.nc"
                className="w-80 rounded-md border px-2 py-1"
              />
              <button
                onClick={onIngestPath}
                className="inline-flex items-center gap-2 rounded-md bg-slate-700 px-3 py-1.5 text-white"
              >
                <HardDriveDownload size={16} /> Ingest Path
              </button>
            </div>
          </div>
          {datasetCtx && (
            <div className="text-xs text-gray-600">
              ActiveDataset → {datasetCtx.parquet_path} • Time {JSON.stringify(datasetCtx.date_range)} • Bounds{' '}
              {JSON.stringify(datasetCtx.spatial_bounds)}
            </div>
          )}
        </div>

        {/* Messages */}
        <div className="flex-1 py-6 overflow-hidden">
          <div className="h-full overflow-y-auto space-y-4 pr-2">
            {messages.map((message, idx) => {
              const showViz = !!datasetCtx && (message.sender === 'bot' || idx === messages.length - 1)
              const bounds = datasetCtx?.spatial_bounds
              const midLon = bounds ? (bounds.lon_min + bounds.lon_max) / 2 : 60
              const midLat = 0
              const range = datasetCtx?.date_range || {}
              const initStart = typeof range.start === 'string' ? range.start.slice(0, 10) : '2010-01-01'
              const initEnd = typeof range.end === 'string' ? range.end.slice(0, 10) : '2013-12-31'
              const initialViz = chooseVizIntent(message.content)

              return (
                <div key={message.id}
                  className={`flex items-start space-x-3 ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                  {message.sender !== 'user' && (
                    <div className="flex-shrink-0">
                      <div className="h-8 w-8 bg-primary-100 rounded-full flex items-center justify-center">
                        <Bot className="h-5 w-5 text-primary-600" />
                      </div>
                    </div>
                  )}

                  <div className={`max-w-2xl px-4 py-3 rounded-lg ${message.sender === 'user' ? 'bg-primary-600 text-white' : 'bg-white border shadow-sm'}`}>
                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                    <div className={`text-xs mt-2 ${message.sender === 'user' ? 'text-primary-100' : 'text-gray-500'}`}>
                      {mounted ? message.tsStr : ''}
                    </div>

                    {showViz && (
                      <ChatViz
                        datasetCtx={datasetCtx}
                        initialViz={initialViz}
                        initLat={midLat}
                        initLon={midLon}
                        initStart={initStart}
                        initEnd={initEnd}
                      />
                    )}
                  </div>

                  {message.sender === 'user' && (
                    <div className="flex-shrink-0">
                      <div className="h-8 w-8 bg-gray-100 rounded-full flex items-center justify-center">
                        <User className="h-5 w-5 text-gray-600" />
                      </div>
                    </div>
                  )}
                </div>
              )
            })}

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
        {messages.length <= 2 && (
          <div className="py-4 border-t bg-white rounded-t-lg">
            <h3 className="text-sm font-medium text-gray-700 mb-3 px-4">Try asking about:</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 px-4">
              {[
                'What is the average temperature at 60°E longitude in 2012?',
                'How does heat content vary between 60°E and 80°E?',
                'Show me the salinity trends in the surface waters',
                'What are the typical temperature ranges in this dataset?',
              ].map((question, index) => (
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

        {/* Composer */}
        <div className="py-4 bg-white border-t">
          <div className="flex items-center space-x-3">
            <div className="flex-1 relative">
              <input
                ref={inputRef}
                type="text"
                value={inputValue}
                onChange={e => setInputValue(e.target.value)}
                onKeyDown={handleKeyPress}
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
          <div className="mt-2 text-xs text-gray-500 px-4">Press Enter to send, Shift+Enter for new line</div>
        </div>
      </div>
    </div>
  )
}
