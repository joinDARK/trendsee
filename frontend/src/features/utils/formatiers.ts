// Форматируем дату в вид ДД.ММ.ГГГГ
export function formatierStringDate(dateString: string): string {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  }).format(date);
}

// Форматируем текст поста. По дефолту до 65 символов
export function formatierText(text: string, max: number = 65): string {
  if (text.length <= max) return text;
  return text.slice(0, max).trimEnd() + '...';
}

// Форматируем id пользователя. По дефолту до 10 символов
export function formatierUserId(userId: string, max: number = 10) {
  if (userId.length <= max) return userId;
  return userId.slice(0, max).trimEnd();
}