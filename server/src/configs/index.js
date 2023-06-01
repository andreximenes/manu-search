export function errorHandler (err, req, res, next) {
  if (err.status === 404)
      res.status(404).json({ url: req.originalUrl, message: " Not found" });
  else
      res.status(500).json({ message: "Something looks wrong :( !!!", error: err});
}

export function createErrorNotFound(req, res, next)  {
  let err = new Error('Not Found');
  err.status = 404;
  next(err);
}

