export function LoadingTransition() {
  return (
    <div className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-white">
      <div className="relative h-48 w-48">
        <div
          className="absolute left-0 top-0 h-16 w-16 animate-bounce rounded-lg bg-sky-400"
          style={{ animationDelay: "0s" }}
        />
        <div
          className="absolute right-0 top-0 h-16 w-16 animate-bounce rounded-lg bg-sky-500"
          style={{ animationDelay: "0.2s" }}
        />
        <div
          className="absolute bottom-0 left-0 h-16 w-16 animate-bounce rounded-lg bg-sky-600"
          style={{ animationDelay: "0.4s" }}
        />
        <div
          className="absolute bottom-0 right-0 h-16 w-16 animate-bounce rounded-lg bg-sky-700"
          style={{ animationDelay: "0.6s" }}
        />
      </div>
      <p className="mt-8 text-lg font-medium text-muted-foreground">Analyzing data...</p>
    </div>
  )
}
