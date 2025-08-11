
if { $argc != 2 || [ lindex $argv 0 ] ne "-path"} {
    puts stderr "Usage: $argv0 -path <logs_root_path>"
    exit 1
}
set root_path [lindex $argv 1]

proc find_log_files {dir} {
    set files {}
    foreach f [glob -nocomplain -directory $dir *] {
        if {[file isdirectory $f]} {
            lappend files {*}[find_log_files $f]
        } elseif {[string match *.log $f]} {
            lappend files $f
        }
    }
    return $files
}

set result {}
set log_files [find_log_files $root_path]

foreach file $log_files {
    set fileData {Error {} Warning {} Info {}}
    set lineNum 0
    set fh [open $file r]
    while {[gets $fh line] >= 0} {
        incr lineNum
        set lowerLine [string tolower $line]
        if {[string match "error:*" $lowerLine]} {
            dict set fileData Error $lineNum $line
        } elseif {[string match "warning:*" $lowerLine]} {
            dict set fileData Warning $lineNum $line
        } elseif {[string match "info:*" $lowerLine]} {
            dict set fileData Info $lineNum $line
        }
    }
    close $fh
    dict set result [file tail $file] $fileData
}

set json "{\n"
foreach fname [dict keys $result] {
    append json "  \"$fname\": {\n"
    foreach category {Error Warning Info} {
        append json "    \"$category\": {\n"

        foreach lineNum [lsort -integer [dict keys [dict get $result $fname $category]]] {
            set content [dict get $result $fname $category $lineNum]

            # Case-insensitive prefix removal (error/warning/info)
            regsub -nocase {^\s*(error|warning|info):\s*} $content {} content

            # Escape double quotes & backslashes
            set content [string map { "\\" "\\\\" "\"" "\\\"" } $content]

            append json "      \"$lineNum\": \"$content\",\n"
        }

        if {[string index $json end] eq "\n"} {
            set json [string trimright $json ",\n"]
            append json "\n"
        }
        append json "    },\n"
    }
    set json [string trimright $json ",\n"]
    append json "\n  },\n"
}
set json [string trimright $json ",\n"]
append json "\n}\n"


set scriptDir [file dirname [file normalize [info script]]]
set outDir [file join $scriptDir ".." "test" "golden"]
file mkdir $outDir
set outFile [file join $outDir "parsed_output.json"]

set fh [open $outFile w]
puts $fh $json
close $fh

puts "JSON saved to $outFile"
