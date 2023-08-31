Bulk Actions with Confirmation Messages User Manual
==================================================

Using the Bulk Actions Feature
-------------------------------

1. **Usage with built-in Sweetalert**

    To use the Bulk Actions feature, add an anchor tag with the `data-toggle="bulk-action"` attribute to your HTML. Customize the attributes for your specific use case. For instance, here's an example of a "Delete Selected" button:

    .. code-block:: html

       <a href="/delete-articles/"
          data-request-method="POST"
          data-toggle="bulk-action"
          data-confirm-message="Are you sure you want to delete the selected articles?"
          data-input-type="selected">Delete Selected</a>

HTML Attributes Summary
-----------------------

Here's a summary of the HTML attributes used in the example:

.. list-table::
   :header-rows: 1

   * - Attribute
     - Is required
     - Options
     - Description
   * - data-toggle="bulk-action"
     - required
     - "bulk-action" (only: "bulk-action")
     - Specifies the use of the "bulk-action" feature.
   * - data-confirm-message
     - required
     - default: "Are you sure you would like to do this action!"
     - Customizable message that appears for confirmation message popup
   * - href
     - required
     -
     - URL for the action.
   * - data-request-method
     - optional
     - selected, queryset, none (default: "selected").
     - Determines the action target items:
       - **selected**: uses selected listing items ids as value
       - **queryset**: uses an object created of url querystring as value
       - **none**: the value is set to null
   * - data-input-type
     - required
     - GET, POST, PUT, DELETE, etc (default: GET).
     - HTTP method for the request.
   * - data-as-form
     - optional
     - default: "false"
     - Submits the request as form (requires a normal http response or redirect, not a json response)
   * - data-force-reload
     - optional
     - default: "true"
     - Reloads the page after action confirmed. When set to "false," it doesn't reload the page and uses the provided "data-callback" to handle the response.
   * - data-callback
     - required with `data-force-reload="false"`
     - default: ''
     - Executes the provided function in its value.
   * - data-confirm-icon
     - optional
     - warning, error, success, info, and question (default: 'warning')
     - Choose an icon for the confirmation modal.
   * - data-confirm-yes
     - optional
     - default: 'Yes, do it!'
     - Sets the popup confirmation dismiss button text.
   * - data-confirm-no
     - optional
     - default: 'No, cancel!'
     - Sets the popup confirmation dismiss button text.
   * - data-cancel-message
     - optional
     - default: "Your action has been cancelled!."
     - The message appears on dismissing the confirmation popup.
   * - data-cancel-icon
     - optional
     - warning, error, success, info, and question (default: 'error')
     - Choose an icon for the cancellation notification.
   * - data-cancel-action
     - optional
     - default: "Ok, got it!"
     - Sets the cancel notification button text.

**Define Callback Function**

Define the callback function, such as `handleDeletionCallback`, which will be called after the action is completed. If `data-force-reload` is set to `false`, the response data is accessible via the `this` keyword:

.. code-block:: html

       <a href="/delete-articles/"
          data-request-method="POST"
          data-toggle="bulk-action"
          data-confirm-message="Are you sure you want to delete the selected articles?"
          data-force-reload="false"
          data-callback="handleDeletionCallback"
          data-input-type="selected">Delete Selected</a>

       <script>
           function handleDeletionCallback() {
           console.log("Bulk deletion completed:", this);
           // Additional handling or notifications can be added here
           }
       </script>


