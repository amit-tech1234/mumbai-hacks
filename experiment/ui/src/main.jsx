import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App, { UserCardsPage, UserInsights } from './App.jsx'
import { createBrowserRouter, RouterProvider } from "react-router-dom"
import './index.css'

import { QueryClient, QueryClientProvider } from 'react-query'

// Create a client
const queryClient = new QueryClient()

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />
  },
  {
    path: '/insights',
    element: <UserCardsPage />
  },
  {
    path: '/:id',
    element: <UserInsights />
  }
])

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </StrictMode>,
)
