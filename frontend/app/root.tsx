import { Outlet } from "react-router"
import appStylesHref from "./app.css?url"
import { authMiddleware } from "./middleware";
import type { Route } from "./+types/root";

export const clientMiddleware: Route.ClientMiddlewareFunction[] = [authMiddleware];

export default function App() {
  return (
    <html>
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="stylesheet" href={appStylesHref} />
        <title>Jobify</title>
      </head>
      <body>
        <Outlet></Outlet>
      </body>
    </html>
  );
}


// import type { Route } from "./+types/root";
// import "./app.css"
// import { Outlet } from "react-router";

// import { authMiddleware } from "./middleware";

// export const clientMiddleware: Route.ClientMiddlewareFunction[] = [authMiddleware];

// export default function App() {
//   return (
//     <html>
//       <head>
//         <title>Jobify</title>
//       </head>
//       <body>
//         <Outlet></Outlet>
//       </body>
//     </html>
//   );
// }