const API_URL = ' https://"API-URL-HERE" ';

export async function fetchItems() {
  try {
    const response = await fetch(API_URL, {
      headers: {
        Authorization: '11223344',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();

    return Array.isArray(data) ? data.slice(-40) : []; // Hämtar de senaste 20 mätningarna
  } catch (error) {
    console.error("Error fetching items:", error);
    return [];
  }
}
