import BackgroundOverlay from "../shared/BackgroundOverlay";

export default function MainLayout({ children }) {
  return (
    <main>
      <div className="relative h-[calc(100vh-64px)] isolate overflow-hidden bg-gray-900">
        <BackgroundOverlay />
        {/* content */}
        <div>{children}</div>
      </div>
    </main>
  );
}
