setTimeout(function() {
    var messages = document.querySelectorAll('.messages');
    messages.forEach(function(message) {
        message.style.display = 'none';
    });
}, 15000);
<script>
    document.getElementById('refreshButton').addEventListener('click', function() {
        document.getElementById('comment').value = '';
    });
</script>