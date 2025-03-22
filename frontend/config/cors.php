<?php

return [

    /*
    |--------------------------------------------------------------------------
    | Cross-Origin Resource Sharing (CORS) Configuration
    |--------------------------------------------------------------------------
    |
    | Here you may configure your settings for cross-origin resource sharing
    | or "CORS". This determines what cross-origin operations may execute
    | in web browsers. You are free to adjust these settings as needed.
    |
    | To learn more: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
    |
    */

    // Define which paths should receive CORS headers. Adjust this if you want it only for specific endpoints.
    'paths' => ['*'],

    // Allowed HTTP methods, '*' means all methods
    'allowed_methods' => ['*'],

    // Allowed origins; set this to your frontend's domain
    'allowed_origins' => ['https://speak-app-ashen.vercel.app/'],

    // Allowed origins patterns (if needed for dynamic matching)
    'allowed_origins_patterns' => [],

    // Allowed headers; '*' means all headers
    'allowed_headers' => ['*'],

    // Headers that are exposed to the browser
    'exposed_headers' => [],

    // Maximum age (in seconds) that the browser should cache the preflight response
    'max_age' => 0,

    // Whether or not the response to the request can be exposed when credentials are present
    'supports_credentials' => false,
];
