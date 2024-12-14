document.addEventListener('DOMContentLoaded', () => {
    const flashMessages = document.querySelectorAll('.flash-message');
    setTimeout(() => {
        flashMessages.forEach(message => {
            message.style.transition = 'opacity 0.5s';
            message.style.opacity = '0';
            setTimeout(() => message.remove(), 500); // Удалить элемент после анимации
        });
    }, 5000); // Сообщения исчезнут через 5 секунд
});
