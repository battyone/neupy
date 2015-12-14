from operator import mul

import theano
import theano.tensor as T

from neupy.algorithms.gd import StepSelectionBuiltIn
from neupy.core.properties import BoundedProperty
from .base import GradientDescent


__all__ = ('Hessian',)


class Hessian(StepSelectionBuiltIn, GradientDescent):
    """ Hessian gradient decent optimization. This GD algorithm
    variation using second derivative information helps choose better
    gradient direction and as a consequence better weight update
    parameter after eqch epoch.

    Parameters
    ----------
    inv_penalty_const : float
        Inverse hessian could be singular matrix. For this reason
        algorithm include penalty that add to hessian matrix identity
        multiplied by defined constant. Defaults to ``1``.
    {GradientDescent.optimizations}
    {ConstructableNetwork.connection}
    {SupervisedConstructableNetwork.error}
    {BaseNetwork.show_epoch}
    {BaseNetwork.shuffle_data}
    {BaseNetwork.epoch_end_signal}
    {BaseNetwork.train_end_signal}
    {Verbose.verbose}

    Methods
    -------
    {BaseSkeleton.predict}
    {SupervisedLearning.train}
    {BaseSkeleton.fit}
    {BaseNetwork.plot_errors}
    {BaseNetwork.last_error}
    {BaseNetwork.last_validation_error}
    {BaseNetwork.previous_error}

    See Also
    --------
    :network:`HessianDiagonal` : Hessian diagonal approximation.
    """
    inv_penalty_const = BoundedProperty(default=1, minval=0)

    def init_properties(self):
        del self.step
        return super(StepSelectionBuiltIn, self).init_properties()

    def init_param_updates(self, layer, parameter):
        parameter_dim = parameter.get_value().shape
        grad = T.grad(self.variables.error_func, wrt=parameter)

        if len(parameter_dim) > 1:
            hessian_dim = mul(*parameter_dim)
        else:
            hessian_dim = parameter_dim[0]

        hessian, _ = theano.scan(
            lambda i, grad, parameter: T.grad(grad[i], wrt=parameter),
            sequences=T.arange(hessian_dim),
            non_sequences=[grad.flatten(), parameter]
        )
        hessian_matrix = hessian.reshape((hessian_dim, hessian_dim))
        hessian_inverse = T.nlinalg.matrix_inverse(
            hessian_matrix + self.inv_penalty_const * T.eye(hessian_dim)
        )

        grad_vector = grad.reshape((hessian_dim, 1))
        parameter_update = hessian_inverse.dot(grad_vector)
        parameter_update = parameter_update.reshape(parameter_dim)

        return [
            (parameter, parameter - parameter_update),
        ]
