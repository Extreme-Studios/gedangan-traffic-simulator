$ErrorActionPreference = 'Stop'
$projectRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..')).TrimEnd('\')
$planPath = Join-Path $projectRoot 'SAFE_DELETE_CANDIDATES.json'
$plan = Get-Content -LiteralPath $planPath -Raw | ConvertFrom-Json
if ($plan.status -ne 'DRY_RUN_VERIFIED' -or $plan.project_root -ne $projectRoot) { throw 'Unverified cleanup plan or incorrect project root.' }
$records = @($plan.candidates)
$targets = @()
# Validate the complete list before the first removal. Never recurse through a junction.
foreach ($record in $records) {
    if ($record.classification -notin @('B','C')) { throw "Protected class: $($record.path)" }
    $absolute = [IO.Path]::GetFullPath((Join-Path $projectRoot $record.path))
    if (-not $absolute.StartsWith($projectRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw "Target escapes workspace: $absolute" }
    $item = Get-Item -LiteralPath $absolute -Force
    if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw "Target is not an ordinary file: $absolute" }
    $parent = $item.Directory
    while ($parent.FullName -ne $projectRoot) {
        if (-not $parent.FullName.StartsWith($projectRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw 'Parent escapes workspace.' }
        if ($parent.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Refusing junction traversal: $($parent.FullName)" }
        $parent = $parent.Parent
    }
    if ($item.Length -ne $record.bytes -or (Get-FileHash -LiteralPath $absolute -Algorithm SHA256).Hash.ToLowerInvariant() -ne $record.sha256) { throw "Changed since inventory: $absolute" }
    $targets += [pscustomobject]@{ absolute=$absolute; record=$record }
}
$started = [DateTimeOffset]::Now.ToString('o')
$deleted = [Collections.Generic.List[object]]::new()
$logPath = Join-Path $PSScriptRoot 'deletion-audit.jsonl'
foreach ($target in $targets) {
    Remove-Item -LiteralPath $target.absolute -Force
    if (Test-Path -LiteralPath $target.absolute) { throw "Deletion was not completed: $($target.absolute)" }
    $entry = [pscustomobject]@{path=$target.record.path; bytes=$target.record.bytes; sha256=$target.record.sha256; classification=$target.record.classification; reason=$target.record.reason; recovery_or_rebuild_method=$target.record.recovery_or_rebuild_method; canonical_copy=$target.record.canonical_copy; deleted_at=[DateTimeOffset]::Now.ToString('o'); verified_absent=$true}
    $deleted.Add($entry)
    Add-Content -LiteralPath $logPath -Value ($entry | ConvertTo-Json -Compress -Depth 6) -Encoding utf8
}
$manifest = [pscustomobject]@{ project_root=$projectRoot; started_at=$started; completed_at=[DateTimeOffset]::Now.ToString('o'); files=$deleted; deleted_count=$deleted.Count; deleted_bytes=($deleted | Measure-Object -Property bytes -Sum).Sum }
$manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $projectRoot 'STORAGE_DELETED_FILES_MANIFEST.json') -Encoding utf8
[pscustomobject]@{ status='DELETION_COMPLETE_REGRESSION_PENDING'; started_at=$started; completed_at=$manifest.completed_at; dry_run_plan_sha256=(Get-FileHash -LiteralPath $planPath -Algorithm SHA256).Hash.ToLowerInvariant(); explicit_file_targets=$targets.Count; deleted_files=$deleted.Count; deleted_bytes=$manifest.deleted_bytes; recursive_deletion_used=$false; outside_workspace_modified=$false; scientific_files_deleted=0; survey_databases_deleted=0; github_uploaded=$false } | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $projectRoot 'STORAGE_CLEANUP_EXECUTION.json') -Encoding utf8
$manifest | Select-Object deleted_count,deleted_bytes | ConvertTo-Json -Compress
