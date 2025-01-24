document.addEventListener('DOMContentLoaded', function() {
    // Обработчики для модальных окон
    const educationModal = new bootstrap.Modal(document.getElementById('educationModal'));
    const experienceModal = new bootstrap.Modal(document.getElementById('experienceModal'));
    const achievementModal = new bootstrap.Modal(document.getElementById('achievementModal'));

    // Обработчики для кнопок открытия модальных окон
    document.querySelector('.add-education')?.addEventListener('click', () => educationModal.show());
    document.querySelector('.add-experience')?.addEventListener('click', () => experienceModal.show());
    document.querySelector('.add-achievement')?.addEventListener('click', () => achievementModal.show());

    // Функция для отправки формы
    async function submitForm(url, formData) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: formData
            });

            const data = await response.json();

            if (data.status === 'success') {
                window.location.reload();
            } else {
                alert('Произошла ошибка при сохранении данных');
                console.error(data.errors);
            }
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Произошла ошибка при отправке данных');
        }
    }

    // Обработчик для сохранения образования
    document.getElementById('saveEducation')?.addEventListener('click', function() {
        const form = document.getElementById('educationForm');
        const formData = new FormData(form);
        submitForm('/accounts/education/add/', formData);
    });

    // Обработчик для сохранения опыта работы
    document.getElementById('saveExperience')?.addEventListener('click', function() {
        const form = document.getElementById('experienceForm');
        const formData = new FormData(form);
        submitForm('/accounts/experience/add/', formData);
    });

    // Обработчик для сохранения достижения
    document.getElementById('saveAchievement')?.addEventListener('click', function() {
        const form = document.getElementById('achievementForm');
        const formData = new FormData(form);
        submitForm('/accounts/achievement/add/', formData);
    });

    // Обработчики для удаления записей
    document.querySelectorAll('.delete-education').forEach(button => {
        button.addEventListener('click', function() {
            if (confirm('Вы уверены, что хотите удалить эту запись об образовании?')) {
                const id = this.dataset.id;
                submitForm(`/accounts/education/${id}/delete/`, new FormData());
            }
        });
    });

    document.querySelectorAll('.delete-experience').forEach(button => {
        button.addEventListener('click', function() {
            if (confirm('Вы уверены, что хотите удалить эту запись об опыте работы?')) {
                const id = this.dataset.id;
                submitForm(`/accounts/experience/${id}/delete/`, new FormData());
            }
        });
    });

    document.querySelectorAll('.delete-achievement').forEach(button => {
        button.addEventListener('click', function() {
            if (confirm('Вы уверены, что хотите удалить это достижение?')) {
                const id = this.dataset.id;
                submitForm(`/accounts/achievement/${id}/delete/`, new FormData());
            }
        });
    });

    // Обработчик для чекбокса "Текущее место работы"
    document.getElementById('is_current')?.addEventListener('change', function() {
        const endDateGroup = document.getElementById('end_date_group');
        const endDateInput = document.getElementById('end_date');
        if (this.checked) {
            endDateGroup.style.display = 'none';
            endDateInput.value = '';
            endDateInput.required = false;
        } else {
            endDateGroup.style.display = 'block';
            endDateInput.required = true;
        }
    });

    // Обработчики для фильтров курсов
    document.querySelectorAll('.filters select').forEach(select => {
        select.addEventListener('change', function() {
            const urlParams = new URLSearchParams(window.location.search);
            urlParams.set(this.name, this.value);
            window.location.search = urlParams.toString();
        });
    });
});
