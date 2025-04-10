'use client'

import { useState } from 'react'
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export default function Chat() {
  const [message, setMessage] = useState('')
  const [chat, setChat] = useState<string[]>([])

  const sendMessage = () => {
    if (message.trim()) {
      setChat([...chat, `You: ${message}`, `Bot: ${message}? That's interesting.`])
      setMessage('')
    }
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-y-auto mb-4 space-y-2">
        {chat.map((line, index) => (
          <div key={index}>{line}</div>
        ))}
      </div>
      <div className="flex space-x-2">
        <Input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type a message"
        />
        <Button onClick={sendMessage}>Send</Button>
      </div>
    </div>
  )
}
