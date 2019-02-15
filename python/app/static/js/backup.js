function get_backup_status() {
    $.post("/admin/api/backup/status", function(data) {
        $("#admin-backup-status").text(data);
    });
}

function generate_backup() {
    $.post("/admin/api/backup/backup", function(data) {
        console.log(data);
        $("#admin-backup-result").text(data);
        get_backup_status();
    });
}

get_backup_status();