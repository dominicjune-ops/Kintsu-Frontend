const componentsConfig = {
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": false,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "client/src/index.css",
    "baseColor": "neutral",
    "cssVariables": true,
    "prefix": ""
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  }
};

const ComponentsConfig = () => {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Components Configuration</h1>
      <pre className="bg-gray-100 p-4 rounded overflow-auto">
        {JSON.stringify(componentsConfig, null, 2)}
      </pre>
    </div>
  );
};

export default ComponentsConfig;