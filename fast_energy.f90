subroutine mindist(a, b, Pos, box, d, Dim, NAtom)
    implicit none

    integer, parameter :: dp=kind(0.d0)    ! double precision

    integer, intent(in)                                 :: Dim, NAtom
    integer, intent(in)                                 :: a, b
    real(dp), intent(in), dimension(0:NAtom-1, 0:Dim-1) :: Pos
    real(dp), intent(in), dimension(0:Dim-1)            :: box
    real(dp), intent(out), dimension(0:Dim-1)           :: d

    d = Pos(a, :) - Pos(b, :)
    if (abs(d(0)) > 0.5_dp*box(0)) then
        if (d(0) > 0.0_dp) then
            d(0) = Pos(a, 0) - (Pos(b, 0) + box(0))
        else if (d(0) < 0.0_dp) then
            d(0) = Pos(a, 0) - (Pos(b, 0) - box(0))
        end if
    end if
    if (abs(d(1)) > 0.5_dp*box(1)) then
        if (d(1) > 0.0_dp) then
            d(1) = Pos(a, 1) - (Pos(b, 1) + box(1))
        else if (d(1) < 0.0_dp) then
            d(1) = Pos(a, 1) - (Pos(b, 1) - box(1))
        end if
    end if
end subroutine

subroutine mindist_norm(a, b, Pos, box, d2, Dim, NAtom)
    implicit none

    integer, parameter :: dp=kind(0.d0)

    integer, intent(in)                                 :: Dim, NAtom
    integer, intent(in)                                 :: a, b
    real(dp), intent(in), dimension(0:NAtom-1, 0:Dim-1) :: Pos
    real(dp), intent(in), dimension(0:Dim-1)            :: box
    real(dp), intent(out)                               :: d2

    real(dp), dimension(0:Dim-1) :: d

    call mindist(a, b, Pos, box, d, Dim, NAtom)
    d2 = sqrt(sum(d**2))
end subroutine

subroutine dist_mat(Pos, box, DMat, Dim, NAtom)
    implicit none

    integer, parameter :: dp=kind(0.d0)

    integer, intent(in)                                    :: Dim, NAtom
    real(dp), intent(in), dimension(0:NAtom-1, 0:Dim-1)    :: Pos
    real(dp), intent(in), dimension(0:Dim-1)               :: box
    real(dp), intent(out), dimension(0:NAtom-1, 0:NAtom-1) :: DMat

    real(dp) :: d2
    integer  :: i, j

    do i = 0, NAtom-1
        do j = 0, NAtom-1
            call mindist_norm(i, j, Pos, box, d2, Dim, NAtom)
            DMat(i, j) = d2
        end do
    end do
end subroutine

subroutine gradient(AMat, DMat, Pos, box, l, grad, Dim, NAtom)
    implicit none

    integer, parameter :: dp=kind(0.d0)

    integer, intent(in)                                     :: Dim, NAtom
    real(dp), intent(in), dimension(0:NAtom-1, 0:NAtom-1)   :: AMat
    real(dp), intent(in), dimension(0:NAtom-1, 0:NAtom-1)   :: DMat
    real(dp), intent(in), dimension(0:NAtom-1, 0:Dim-1)     :: Pos
    real(dp), intent(in), dimension(0:Dim-1)                :: box
    real(dp), intent(in)                                    :: l
    real(dp), intent(inout), dimension(0:NAtom-1, 0:Dim-1)  :: grad
!f2py intent(in, out) :: grad

    integer                      :: i, j
    real(dp), dimension(0:Dim-1) :: d, fac

    do i = 0, NAtom-1
        do j =0, NAtom-1
            call mindist(i, j, Pos, box, d, Dim, NAtom)
            fac(:) = d(:) * (1.0_dp - l/DMat(i, j))
            grad(i, :) = grad(i, :) + AMat(i, j) * fac(:) + AMat(j, i) * fac(:)
        end do
    end do
end subroutine
