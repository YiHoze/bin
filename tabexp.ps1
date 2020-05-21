﻿Function TabExpansion2 {
    [CmdletBinding(DefaultParameterSetName = 'ScriptInputSet')]
    Param(
        [Parameter(ParameterSetName = 'ScriptInputSet', Mandatory = $true, Position = 0)]
        [string] $inputScript,

        [Parameter(ParameterSetName = 'ScriptInputSet', Mandatory = $true, Position = 1)]
        [int] $cursorColumn,

        [Parameter(ParameterSetName = 'AstInputSet', Mandatory = $true, Position = 0)]
        [System.Management.Automation.Language.Ast] $ast,

        [Parameter(ParameterSetName = 'AstInputSet', Mandatory = $true, Position = 1)]
        [System.Management.Automation.Language.Token[]] $tokens,

        [Parameter(ParameterSetName = 'AstInputSet', Mandatory = $true, Position = 2)]
        [System.Management.Automation.Language.IScriptPosition] $positionOfCursor,

        [Parameter(ParameterSetName = 'ScriptInputSet', Position = 2)]
        [Parameter(ParameterSetName = 'AstInputSet', Position = 3)]
        [Hashtable] $options = $null
    )

    End
    {
        $source = $null
        if ($psCmdlet.ParameterSetName -eq 'ScriptInputSet')
        {
            $source = [System.Management.Automation.CommandCompletion]::CompleteInput(
                <#inputScript#>  $inputScript,
                <#cursorColumn#> $cursorColumn,
                <#options#>      $options)
        }
        else
        {
            $source = [System.Management.Automation.CommandCompletion]::CompleteInput(
                <#ast#>              $ast,
                <#tokens#>           $tokens,
                <#positionOfCursor#> $positionOfCursor,
                <#options#>          $options)
        }
        $field = [System.Management.Automation.CompletionResult].GetField('completionText', 'Instance, NonPublic')
        $source.CompletionMatches | ForEach-Object {
            $item = $_.CompletionText
            $ext = [io.path]::GetExtension($item)
            $cnt = ($item.ToCharArray() | Where-Object {$_ -eq '\'} | Measure-Object).Count
            # write-host $item, $cnt
            # only at the current directory
            if ($cnt -eq 1) {            
                If ($ext -ne '.cmd' -and $ext -ne '.bat' -and $ext -ne '.ps1' -and $ext -ne '.exe') {
                    $field.SetValue($_, [io.path]::GetFileName($_.CompletionText))                    
                }
            }                        
        }
        Return $source
    }    
}