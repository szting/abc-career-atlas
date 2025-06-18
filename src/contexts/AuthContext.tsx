import React, { createContext, useContext, useState, useEffect } from 'react'
import Cookies from 'js-cookie'

interface User {
  username: string
  isAdmin: boolean
}

interface AuthContextType {
  user: User | null
  login: (username: string, password: string) => boolean
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

const users = {
  demo: { password: 'demo123', isAdmin: false },
  admin: { password: 'admin123', isAdmin: true }
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)

  useEffect(() => {
    const savedUser = Cookies.get('user')
    if (savedUser) {
      setUser(JSON.parse(savedUser))
    }
  }, [])

  const login = (username: string, password: string): boolean => {
    const userInfo = users[username as keyof typeof users]
    if (userInfo && userInfo.password === password) {
      const userData = { username, isAdmin: userInfo.isAdmin }
      setUser(userData)
      Cookies.set('user', JSON.stringify(userData), { expires: 7 })
      return true
    }
    return false
  }

  const logout = () => {
    setUser(null)
    Cookies.remove('user')
  }

  return (
    <AuthContext.Provider value={{
      user,
      login,
      logout,
      isAuthenticated: !!user
    }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
