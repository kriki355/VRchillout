# Простой веб-сервер для теста: отдаёт папку site на http://localhost:8080
$root = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) 'site'
$port = 8080
$types = @{ '.html'='text/html; charset=utf-8'; '.js'='application/javascript'; '.css'='text/css'; '.png'='image/png'; '.jpg'='image/jpeg'; '.json'='application/json'; '.webmanifest'='application/manifest+json'; '.svg'='image/svg+xml'; '.glb'='model/gltf-binary' }
$l = New-Object System.Net.HttpListener
$l.Prefixes.Add("http://localhost:$port/")
try { $l.Start() } catch { Write-Host "Не удалось занять порт $port. Закройте другие окна сервера и запустите снова."; Read-Host "Enter — выход"; exit 1 }
Write-Host ""
Write-Host "  Сервер работает: http://localhost:$port"
Write-Host "  Не закрывайте это окно, пока тестируете."
Write-Host ""
while ($l.IsListening) {
  $ctx = $l.GetContext()
  $rel = [Uri]::UnescapeDataString($ctx.Request.Url.AbsolutePath.TrimStart('/'))
  if ($rel -eq '') { $rel = 'index.html' }
  $file = [IO.Path]::GetFullPath((Join-Path $root $rel))
  if ($file.StartsWith($root) -and (Test-Path $file -PathType Leaf)) {
    $bytes = [IO.File]::ReadAllBytes($file)
    $ext = [IO.Path]::GetExtension($file).ToLower()
    $ctx.Response.ContentType = $(if ($types[$ext]) { $types[$ext] } else { 'application/octet-stream' })
    $ctx.Response.Headers.Add('Cache-Control','no-store')
    $ctx.Response.ContentLength64 = $bytes.Length
    $ctx.Response.OutputStream.Write($bytes, 0, $bytes.Length)
    Write-Host ("  " + (Get-Date -Format HH:mm:ss) + "  " + $rel)
  } else { $ctx.Response.StatusCode = 404 }
  $ctx.Response.Close()
}
