(defun what-line ()
  "Print the current buffer line number and narrowed line number of point."
  (interactive)
  (let ((start (- (point-min) 1))
	(n (- (line-number-at-pos) 1)))
    (if (= start 0)
	(message "Line %d" n)
      (save-excursion
	(save-restriction
	  (widen)
	  (message "line %d (narrowed line %d)"
		 (+ n (line-number-at-pos start) -1) n))))))
