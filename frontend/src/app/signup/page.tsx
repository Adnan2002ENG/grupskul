"use client"

import { useState } from "react"
import { supabase } from "@/lib/supabase"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Card, CardContent } from "@/components/ui/card"

export default function SignupPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [message, setMessage] = useState("")

  const handleSignup = async () => {
    const { error } = await supabase.auth.signUp({ email, password })
    setMessage(error ? error.message : "Signup successful! Please check your email.")
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-gray-900">
      <Card className="w-full max-w-md p-6 shadow-md border border-gray-200 dark:border-gray-700">
        <CardContent>
          <h1 className="text-2xl font-bold mb-6 text-center">Create your account</h1>
          <div className="space-y-4">
            <div>
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="you@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
            <div>
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
            <Button className="w-full mt-4" onClick={handleSignup}>
              Sign Up
            </Button>
            {message && (
              <p className="text-sm text-center text-red-500 dark:text-red-400 mt-2">{message}</p>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
