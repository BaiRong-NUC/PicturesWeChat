const { createApp, ref, onMounted, onUnmounted } = Vue;
createApp({
    setup() {
        const events = ref([]);
        const loading = ref(false);
        const lastUpdated = ref("");
        const preview = ref(null);
        let timer = null;

        const fetchEvents = async () => {
            loading.value = true;
            try {
                const res = await fetch("/api/events");
                const data = await res.json();
                events.value = data.events || [];
                lastUpdated.value = new Date().toLocaleTimeString();
            } catch (err) {
                console.error("fetch events failed:", err);
            } finally {
                loading.value = false;
            }
        };

        const clearAll = async () => {
            if (!confirm("确认要清空所有陌生人记录吗？")) return;
            await fetch("/api/events/clear", { method: "POST" });
            await fetchEvents();
        };

        onMounted(() => {
            fetchEvents();
            timer = window.setInterval(fetchEvents, 5000);
        });

        onUnmounted(() => {
            if (timer !== null) {
                clearInterval(timer);
            }
        });

        return {
            events,
            loading,
            lastUpdated,
            preview,
            fetchEvents,
            clearAll,
        };
    },
}).mount("#app");
