// class sytnax is to be used sparingly
export class HttpError extends Error {
  /**
   *
   * @param {String} [message] - error message
   */
  constructor(message) {
    super(message);
    //watch this during minfication
    this.name = this.constructor.name;
    Object.setPrototypeOf(this, new.target.prototype);

    // only works for chrome (and other v8 browsers). TODO fix stack for mozilla
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, this.constructor);
    }
  }
}

export class NotImplementedError extends Error {
  /**
   *
   */

  constructor(message = "Not Implemented") {
    super(message);
    //watch this during minfication
    this.name = this.constructor.name;
    Object.setPrototypeOf(this, new.target.prototype);

    // only works for chrome (and other v8 browsers). TODO fix stack for mozilla
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, this.constructor);
    }
  }
}
