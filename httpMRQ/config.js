var base_config = {
  redis_config: {
    host: "127.0.0.1",
    port: 6379,
    auth: '',
    subscribe_key: 'dms_hub',
    topic_key: 'dms_topic',
  },
  log4js_config: {
    "appenders": [{
      "type": "console",
      "category": "console",
      "filename": "./logs/console.log",
      "maxLogSize": 104800,
      "backups": 100
    },
    {
      "category": "log_file",
      "type": "file",
      "filename": "./logs/log_file.log",
      "maxLogSize": 104800,
      "backups": 100
    },
    {
      "category": "log_date",
      "type": "dateFile",
      "filename": "./logs/date",
      "alwaysIncludePattern": true,
      "pattern": "-yyyy-MM-dd-hh.log"

    }],
    "replaceConsole": true,
    "levels": {
      "log_file": "ALL",
      "console": "ALL",
      "log_date": "ALL"
    }
  }
};

exports.config = base_config;