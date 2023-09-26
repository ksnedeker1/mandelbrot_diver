# mandelbrot_diver

A simple multithreaded Mandelbrot fractal renderer using the Qt framework for threading and GUI management, alongside
numpy for vectorized numerical computations.

### Features

* **Parallel Processing**: Using PyQt's QThreadPool, the renderer subdivides the currently-viewed partitions of the set
into chunks and assigns each to a worker thread, allowing for simultaneous computation and faster rendering.
* **Real-Time Rendering**: As each thread completes its assigned chunk, the results are immediately spliced into the
display array. User actions that change the display area automatically result in new worker tasks for updated chunks.
* **Dynamic Loading**: The pool manager automatically starts worker threads and halts any ongoing threads which are no 
longer needed.
* **Vectorized Computations**: Numpy's native vectorization allows for quicker operations during the identification 
of non-diverged points, the updating of set iteration counts and masking of bounded points with boolean indexing, and 
the updating of non-diverged iteration counts.
* **Interactiveness**: Zooming is cursor-oriented, allowing for a more intuitive user experience whereby a zoom-in or 
zoom-out action will be centered around the user's cursor at the time of the event. Multiple color mappings are 
available for different manners of interpretation.

### Plans for Expansion
* **Dynamic Thread Allocation and Sizing**: Increase efficiency by dynamically allocating threads based on system 
capabilities and computational complexity.
* **GPU Acceleration**: Offer GPU-based computation for compatible users.
* **Dynamic Level of Detail**: Introduce varying degrees of detail based on zoom level by updating the max iteration 
count to the most appropriate value.
* **Expanded Interactions**: Implement additional GUI features such as click-and-drag panning, saving specific views, 
or allowing for the passing of custom parameters.
* **Profiling and Benchmarking**: Track performance to aid in optimizing that renderer's performance and offer metrics
to users.