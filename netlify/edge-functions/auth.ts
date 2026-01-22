import type { Context } from "https://edge.netlify.com";

export default async (request: Request, context: Context) => {
  // Get credentials from environment variables
  const USERNAME = Netlify.env.get("SITE_USERNAME") || "admin";
  const PASSWORD = Netlify.env.get("SITE_PASSWORD");
  
  // Skip auth if no password is set (useful for preview deploys)
  if (!PASSWORD) {
    return context.next();
  }
  
  const authHeader = request.headers.get("authorization");
  
  if (!authHeader) {
    return new Response("Authentication required", {
      status: 401,
      headers: {
        "WWW-Authenticate": 'Basic realm="Career Framework - Please Login"',
      },
    });
  }
  
  const base64Credentials = authHeader.split(" ")[1];
  const credentials = atob(base64Credentials);
  const [username, password] = credentials.split(":");
  
  if (username === USERNAME && password === PASSWORD) {
    // Allow the request to proceed
    return context.next();
  }
  
  return new Response("Invalid credentials", {
    status: 401,
    headers: {
      "WWW-Authenticate": 'Basic realm="Career Framework - Please Login"',
    },
  });
};

export const config = { path: "/*" };
