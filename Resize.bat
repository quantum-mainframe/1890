cmd.exe /K
mkdir Resized
for %f in (*.png) do ffmpeg -i "%~nxf" -s 300x300 "Resized\%~nxf"