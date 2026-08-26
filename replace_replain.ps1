$oldScript = "<script type='text/javascript' data-cfasync='false'>window.purechatApi = { l: [], t: [], on: function () { this.l.push(arguments); } }; (function () { var done = false; var script = document.createElement('script'); script.async = true; script.type = 'text/javascript'; script.src = 'https://app.purechat.com/VisitorWidget/WidgetScript'; document.getElementsByTagName('HEAD').item(0).appendChild(script); script.onreadystatechange = script.onload = function (e) { if (!done && (!this.readyState || this.readyState == 'loaded' || this.readyState == 'complete')) { var w = new PCWidget({c: '76adb4c9-78ac-4ea9-b7b3-36e4412eca7d', f: true }); done = true; } }; })();</script>"

$newScript = @"
<script>
window.replainSettings = { id: '49635770-b7b9-49c1-bb08-348efe34892c' };
(function(u){var s=document.createElement('script');s.async=true;s.src=u;
var x=document.getElementsByTagName('script')[0];x.parentNode.insertBefore(s,x);
})('https://widget.replain.cc/dist/client.js');
</script>
"@

$files = Get-ChildItem -Path ".\" -Filter "*.html" -Recurse

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    if ($content -match [regex]::Escape($oldScript)) {
        $content = $content -replace [regex]::Escape($oldScript), $newScript
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8
        Write-Output "Replaced in $($file.FullName)"
    }
}
