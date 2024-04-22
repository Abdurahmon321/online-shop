function sendMessage(data) {
    // Xabarni yuborish uchun serverga so'rov yuborish
    fetch('/chat/sender/{{ request.user.id }}/receiver/{{ user.id }}/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}' // Agar CSRF to'kenni kerak bo'lsa
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (response.ok) {
            // Xabar muvaffaqiyatli yuborilgan
            console.log('Message sent successfully');
            // O'zgartirishlar uchun kerakli ishlarni bajarish
        } else {
            // Xatolik yuz berdi
            console.error('Failed to send message');
        }
    })
    .catch(error => {
        // Ishonchsiz xatolik
        console.error('Error:', error);
    });
}
