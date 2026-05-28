$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$port = 8787
$prefix = "http://localhost:$port/"

Add-Type -AssemblyName System.Web

$listener = [System.Net.HttpListener]::new()
$listener.Prefixes.Add($prefix)

try {
  $listener.Start()
} catch {
  Write-Host "Could not start local app server on $prefix"
  Write-Host "Another app may already be using port $port."
  Read-Host "Press Enter to close"
  exit 1
}

Start-Process $prefix
Write-Host "CNC Cell Planner is running at $prefix"
Write-Host "Keep this window open while using the app. Press Ctrl+C to stop."

function Get-ContentType($path) {
  switch ([System.IO.Path]::GetExtension($path).ToLowerInvariant()) {
    ".html" { "text/html; charset=utf-8"; break }
    ".js" { "text/javascript; charset=utf-8"; break }
    ".json" { "application/json; charset=utf-8"; break }
    ".png" { "image/png"; break }
    ".txt" { "text/plain; charset=utf-8"; break }
    default { "application/octet-stream" }
  }
}

try {
  while ($listener.IsListening) {
    $ctx = $listener.GetContext()
    $rawPath = [System.Web.HttpUtility]::UrlDecode($ctx.Request.Url.AbsolutePath.TrimStart("/"))
    if ([string]::IsNullOrWhiteSpace($rawPath)) { $rawPath = "index.html" }
    $safePath = $rawPath -replace "/", [System.IO.Path]::DirectorySeparatorChar
    $fullPath = [System.IO.Path]::GetFullPath((Join-Path $root $safePath))

    if (!$fullPath.StartsWith($root, [System.StringComparison]::OrdinalIgnoreCase) -or !(Test-Path -LiteralPath $fullPath -PathType Leaf)) {
      $ctx.Response.StatusCode = 404
      $bytes = [System.Text.Encoding]::UTF8.GetBytes("Not found")
    } else {
      $ctx.Response.StatusCode = 200
      $ctx.Response.ContentType = Get-ContentType $fullPath
      $bytes = [System.IO.File]::ReadAllBytes($fullPath)
    }

    $ctx.Response.ContentLength64 = $bytes.Length
    $ctx.Response.OutputStream.Write($bytes, 0, $bytes.Length)
    $ctx.Response.OutputStream.Close()
  }
} finally {
  $listener.Stop()
}
