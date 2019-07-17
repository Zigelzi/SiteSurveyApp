document.addEventListener('DOMContentLoaded', () => {
    const coordinatesButton = document.getElementById('btn-coords')

    function getCoords() {
        // Function to get users coordinates and input them to the lateral and longitudal form fields
        const coordinateFieldLat = document.getElementById('coordinate_lat');
        const coordinateFieldLong = document.getElementById('coordinate_long');
        const coordinateError = document.getElementById('error');

        function success(position) {
            // Success callback if the navigator is able to return the location
            const lat = position.coords.latitude;
            const long = position.coords.longitude;

            coordinateError.textContent = '';
            coordinateFieldLat.value = lat;
            coordinateFieldLong.value = long;
        }

        function error () {
            // Error callback if navigator is not able to locate the user
            coordinateError.textContent = 'Unable to retrieve your location';
        }

        if (!navigator.geolocation) {
            // Check if the navigator is supported by users browser and run it if it is
            coordinateError.textContent = 'Geolocation is not supported by your browser';
        } else {
            navigator.geolocation.getCurrentPosition(success, error);
        }
    }

    coordinatesButton.addEventListener('click', getCoords);
})