param(
  [Parameter(Mandatory=$true)][string]$Jdk,
  [Parameter(Mandatory=$true)][string]$Platform,
  [Parameter(Mandatory=$true)][string]$BuildTools
)
$ErrorActionPreference = 'Stop'
$projectRoot = $PSScriptRoot
$outputDir = Join-Path $projectRoot '.build'
$classesDir = Join-Path $outputDir 'classes'
$signingDir = Join-Path $projectRoot '.signing'
New-Item -ItemType Directory -Force $classesDir,$signingDir | Out-Null
function Run-Tool([string]$Program, [string[]]$Arguments) {
  & $Program @Arguments
  if ($LASTEXITCODE -ne 0) { throw "$Program failed: $LASTEXITCODE" }
}
$javaFiles = @(Get-ChildItem -LiteralPath (Join-Path $projectRoot 'app/src/main/java') -Filter '*.java' -Recurse | ForEach-Object FullName)
$androidJar = Join-Path $Platform 'android.jar'
Run-Tool (Join-Path $Jdk 'bin/javac.exe') (@('-encoding','UTF-8','-source','8','-target','8','-classpath',$androidJar,'-d',$classesDir) + $javaFiles)
$classFiles = @(Get-ChildItem -LiteralPath $classesDir -Filter '*.class' -Recurse | ForEach-Object FullName)
Run-Tool (Join-Path $Jdk 'bin/java.exe') (@('-cp',(Join-Path $BuildTools 'lib/d8.jar'),'com.android.tools.r8.D8','--lib',$androidJar,'--min-api','26','--output',$outputDir) + $classFiles)
$unsignedApk = Join-Path $outputDir 'sensor-unsigned.apk'
$manifestDoc = [xml](Get-Content -LiteralPath (Join-Path $projectRoot 'app/src/main/AndroidManifest.xml') -Raw)
$manifestDoc.manifest.SetAttribute('package','org.nodestomaps.sensor')
$buildManifest = Join-Path $outputDir 'AndroidManifest.xml'
$manifestDoc.Save($buildManifest)
Run-Tool (Join-Path $BuildTools 'aapt2.exe') @('link','--manifest',$buildManifest,'-I',$androidJar,'--min-sdk-version','26','--target-sdk-version','35','--version-code','1','--version-name','0.1.0','-o',$unsignedApk)
Push-Location $outputDir
try { Run-Tool (Join-Path $Jdk 'bin/jar.exe') @('uf',$unsignedApk,'classes.dex') } finally { Pop-Location }
$alignedApk = Join-Path $outputDir 'sensor-aligned.apk'
Run-Tool (Join-Path $BuildTools 'zipalign.exe') @('-f','4',$unsignedApk,$alignedApk)
$keystore = Join-Path $signingDir 'classroom-debug.jks'
if (!(Test-Path -LiteralPath $keystore)) {
  Run-Tool (Join-Path $Jdk 'bin/keytool.exe') @('-genkeypair','-keystore',$keystore,'-storepass','android','-keypass','android','-alias','classroom','-keyalg','RSA','-keysize','2048','-validity','3650','-dname','CN=Nodes to Maps Classroom Debug')
}
$finalApk = Join-Path $outputDir 'nodes-to-maps-sensor-debug.apk'
Run-Tool (Join-Path $Jdk 'bin/java.exe') @('-jar',(Join-Path $BuildTools 'lib/apksigner.jar'),'sign','--ks',$keystore,'--ks-key-alias','classroom','--ks-pass','pass:android','--key-pass','pass:android','--out',$finalApk,$alignedApk)
Run-Tool (Join-Path $Jdk 'bin/java.exe') @('-jar',(Join-Path $BuildTools 'lib/apksigner.jar'),'verify','--verbose',$finalApk)
Get-FileHash -LiteralPath $finalApk -Algorithm SHA256
Write-Output "Classroom test APK: $finalApk"
