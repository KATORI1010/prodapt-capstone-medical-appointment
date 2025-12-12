import { NavLink, Outlet, redirect, type ClientLoaderFunctionArgs } from "react-router";
import type { Route } from "../+types/root";
import { userContext } from "~/context";

import { Hospital } from 'lucide-react';
import { Avatar, AvatarImage } from "~/components/ui/avatar";

export async function clientLoader({ context }: ClientLoaderFunctionArgs) {
  // const me = context.get(userContext);
  // const isAdmin = me && me.is_admin;
  const isAdmin = true;
  return { isAdmin }
}


export default function DefaultLayout({ loaderData }: Route.ComponentProps) {
  const navLinkStyle =
    ({ isActive }) => {
      return (isActive
        ? "rounded-md px-4 py-2 font-semibold bg-gray-200 text-gray-700 hover:bg-gray-300 transition"
        : "rounded-md px-4 py-2"
      )
    }
  return (
    <main>
      <nav className="flex items-center gap-4 w-full h-16 px-4 border-b">
        <Hospital size="40px" className="ml-2" />
        <NavLink to="/" className={navLinkStyle}>Home</NavLink>
        <NavLink to="/job-boards" className={navLinkStyle}>JobBoards</NavLink>

        {loaderData.isAdmin
          ? <NavLink to="/admin-logout" className={navLinkStyle}>Logout</NavLink>
          : <NavLink to="/admin-login" className={navLinkStyle}>Login</NavLink>
        }
      </nav>
      <Outlet />
    </main>
  );
}
