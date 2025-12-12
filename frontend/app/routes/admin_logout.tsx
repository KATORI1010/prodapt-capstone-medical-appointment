import { redirect, type ClientLoaderFunctionArgs } from "react-router"
import { userContext } from "../context"

export async function clientLoader({ context }: ClientLoaderFunctionArgs) {
    await fetch(`/api/admin-logout`, {
        method: 'POST',
    })
    context.set(userContext, null)
    return redirect("/job-boards")
}

export default function Logout() {
    return <></>
}