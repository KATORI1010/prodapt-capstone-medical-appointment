import { userContext } from "./context"

export async function authMiddleware({ context } , next ) { 
  const existingMe = context.get(userContext)
  if (existingMe){
    return next()
  }
  const response = await fetch("/api/me")
  const me = await response.json()
  context.set(userContext, me)
  return next()
}
