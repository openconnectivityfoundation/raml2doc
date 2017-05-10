var $RefParser = require('json-schema-ref-parser');

$RefParser.bundle(process.argv[2])
  .then(function(schema) {
    console.log(JSON.stringify(schema));
  });
