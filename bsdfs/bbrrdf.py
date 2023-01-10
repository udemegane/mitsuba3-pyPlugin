import mitsuba as mi
import drjit as dr

class BBRRDF(mi.BSDF):
    def __init__(self, props: mi.Properties):
        mi.BSDF.__init__(self, props)
        assert(props.has_property('reflectance'))
        self.reflectance = props['reflectance']
        self.m_flags = mi.BSDFFlags.DiffuseReflection | mi.BSDFFlags.FrontSide
        self.m_components = [self.m_flags]

    def sample(self, ctx, si, sample1, sample2, active):
        bsdfSample = mi.BSDFSample3f()
        bsdfSample.wo = mi.warp.square_to_cosine_hemisphere(sample1)
        bsdfSample.pdf = mi.warp.square_to_cosine_hemisphere_pdf(bsdfSample.wo)
        bsdfSample.eta = 1.0
        bsdfSample.sampled_type = mi.UInt32(+mi.BSDFFlags.DiffuseReflection)
        bsdfSample.sampled_component = mi.UInt32(0)
        value = 0.0
        return (bsdfSample, value)

    def eval(self, ctx, si, wo, active):
        return 0.0

    def pdf(self, ctx, si, wo, active):
        if not ctx.is_enabled(mi.BSDFFlags.DiffuseReflection):
            return 0.0
        cos_theta_i = mi.Frame3f.cos_theta(si.wi)
        cos_theta_o = mi.Frame3f.cos_theta(wo)
        pdf = mi.warp.square_to_cosine_hemisphere_pdf(wo)
        return dr.select(cos_theta_i > 0.0 and cos_theta_o > 0.0, pdf, 0.0)

    def travarse(self, callback):
        callback.put_parameter()

    def to_string(self):
        return "BBRRDF[reflectance=%s]" % self.reflectance